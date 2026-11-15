"""Bộ kiểm cuối: lô của bạn đã đủ điều kiện nộp chưa? (đối chiếu checklist 5 mục của slide Day 10).

    python scripts/check_batch.py            # in từng kiểm tra PASS / WARN / FAIL
    python scripts/check_batch.py --json out.json

Exit code 1 nếu còn FAIL. Script này CHỈ KIỂM, không sửa gì. Nó biết định dạng đúng, KHÔNG biết nhãn có đúng hay không
(việc đó là QC của người) và không chấm chất lượng lời giải thích của bạn (người chấm đọc).
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ANNOT_RE, GUIDE_RE, ROOT, STARTER, SUBMISSION, batch_dir, find_annotation_file, jpeg_size,  # noqa: E402
                    list_files, load_config, parse_img_name, parse_readme_txt, read_csv, sha256_file, vn_int, BATCH_RE)
from pack_batch import build_zip  # noqa: E402

WORK = SUBMISSION / "worklog"
ANA = SUBMISSION / "analysis"
CONCL = ("Release", "Hold", "Rework")
README_KEYS = ["Lô", "Ngày nộp", "Người nộp", "Số ảnh", "Số nhãn", "Guideline", "Định dạng", "QC", "Ghi chú"]
PHIEU_KEYS = ["Tên lô", "Ngày", "Số ảnh", "Số nhãn", "Guideline", "QC", "SHA-256 zip", "Kết luận"]
ALLOWED_TOP = {"images", "annotations", "manifest.csv", "label_summary.csv", "qc_report.txt", "README.txt", "truyvet.csv",
               "ATTRIBUTION.csv"}


class R:
    def __init__(self) -> None:
        self.rows: List[dict] = []

    def add(self, cid: str, status: str, msg: str, group: str) -> None:
        self.rows.append(dict(id=cid, status=status, msg=msg, group=group))

    def ok(self, cid, msg, g): self.add(cid, "PASS", msg, g)
    def bad(self, cid, msg, g): self.add(cid, "FAIL", msg, g)
    def warn(self, cid, msg, g): self.add(cid, "WARN", msg, g)

    def check(self, cid, cond, good, bad, g):
        (self.ok if cond else self.bad)(cid, good if cond else bad, g)
        return cond


def parse_kv(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = re.sub(r"^\s*[-*]\s*", "", line.replace("**", "")).strip()
        m = re.match(r"^([^:|]{2,40}?):\s*(.*)$", s)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out


def short(items, n=4):
    items = list(items)
    return ", ".join(str(i) for i in items[:n]) + (f" … (+{len(items) - n})" if len(items) > n else "")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json")
    args = ap.parse_args()
    cfg = load_config()
    bid = cfg["batch_id"]
    bd = batch_dir(cfg)
    r = R()
    G = {"A": "A. Cấu trúc lô (4 phần)", "B": "B. Kiểm file xuất (4 câu)", "C": "C. Manifest và hash",
         "D": "D. Metadata và truy vết", "E": "E. Số liệu README/QC nhất quán", "F": "F. Phiếu, checklist, bảo mật",
         "G": "G. Bằng chứng làm việc"}

    # ------------------------------------------------------------------ A
    if not r.check("A1", bd.is_dir(), f"thư mục lô {bid}/ tồn tại", f"không thấy submission/{bid}/", G["A"]):
        finish(r, args)
    private = bool(cfg.get("images_private", False))
    top = {p.name for p in bd.iterdir() if not p.name.startswith(".") and p.name.lower() not in ("thumbs.db", "desktop.ini")}
    stray = sorted(top - ALLOWED_TOP)
    r.check("A2", not stray, "không có file lạ ngoài cấu trúc lô", f"file/thư mục lạ trong lô: {short(stray)}", G["A"])
    need = ["manifest.csv", "label_summary.csv", "qc_report.txt", "README.txt", "truyvet.csv"]
    miss = [n for n in need if not (bd / n).is_file()]
    r.check("A3", not miss, "đủ manifest, label_summary, qc_report, README, truyvet", f"thiếu: {short(miss)}", G["A"])
    ann = find_annotation_file(bd)
    ann_n = len(list((bd / "annotations").glob("*.json"))) if (bd / "annotations").is_dir() else 0
    r.check("A4", ann_n == 1, "đúng một file nhãn trong annotations/", f"annotations/ có {ann_n} file .json (cần đúng 1)", G["A"])
    ver = BATCH_RE.match(bid).group(2)
    if ann:
        r.check("A5", ann.name == f"instances_v{ver}.json", f"tên file nhãn {ann.name} khớp phiên bản lô",
                f"file nhãn tên {ann.name}, cần instances_v{ver}.json", G["A"])
    imgs_dir = bd / "images"
    img_files = [p.name for p in list_files(imgs_dir)]
    if private:
        r.warn("A6", "images_private=true: bỏ kiểm thư mục images/ (phải giải thích ở security.md)", G["A"])
    else:
        r.check("A6", bool(img_files), f"images/ có {len(img_files)} file", "images/ trống hoặc không tồn tại", G["A"])

    # ------------------------------------------------------------------ B
    d = None
    if ann:
        try:
            d = json.loads(ann.read_text(encoding="utf-8"))
            ok = all(k in d for k in ("images", "annotations", "categories"))
            r.check("B1", ok, "file nhãn mở lại được, đủ images/annotations/categories", "JSON mở được nhưng thiếu khoá bắt buộc", G["B"])
            if not ok:
                d = None
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            r.bad("B1", f"file nhãn không đọc được: {e}", G["B"])
    labels_total, per_class = 0, {}
    if d and private:
        img_files = sorted(i["file_name"] for i in d["images"])
    if d:
        cname = {c["id"]: c["name"] for c in d["categories"]}
        names = list(cname.values())
        extra = [n for n in names if n not in cfg["classes"]]
        r.check("B2", not extra, f"mọi tên lớp thuộc taxonomy {cfg['classes']}",
                f"tên lớp ngoài taxonomy (so từng ký tự): {[repr(x) for x in extra]}", G["B"])
        unk = [a["id"] for a in d["annotations"] if a["category_id"] not in cname]
        r.check("B2b", not unk, "mọi nhãn trỏ tới category có thật", f"{len(unk)} nhãn trỏ category không tồn tại", G["B"])
        for a in d["annotations"]:
            n = cname.get(a["category_id"], "?")
            per_class[n] = per_class.get(n, 0) + 1
        labels_total = len(d["annotations"])
        ids = [a["id"] for a in d["annotations"]]
        r.check("B3", len(ids) == len(set(ids)), "id nhãn không trùng", "id nhãn bị trùng", G["B"])
        coco_names = [i["file_name"] for i in d["images"]]
        miss_f = [] if private else sorted(set(coco_names) - set(img_files))
        extra_f = [] if private else sorted(set(img_files) - set(coco_names))
        r.check("B4", not miss_f and not extra_f and len(coco_names) == len(set(coco_names)),
                f"ảnh trong file nhãn khớp images/ ({len(coco_names)} ảnh)",
                f"lệch: file nhãn có mà images/ không có {short(miss_f)}; images/ có mà file nhãn không {short(extra_f)}", G["B"])
        iid = {i["id"]: i for i in d["images"]}
        bad_ref = [a["id"] for a in d["annotations"] if a["image_id"] not in iid]
        r.check("B5", not bad_ref, "mọi nhãn trỏ tới ảnh có thật", f"{len(bad_ref)} nhãn trỏ image_id không tồn tại", G["B"])
        out, deg = [], []
        for a in d["annotations"]:
            im = iid.get(a["image_id"])
            if not im:
                continue
            x, y, w, h = a["bbox"]
            if w <= 0 or h <= 0:
                deg.append(a["id"])
            elif x < 0 or y < 0 or x + w > im["width"] + 1e-6 or y + h > im["height"] + 1e-6:
                out.append(a["id"])
        r.check("B6", not out, "không có box nằm ngoài ảnh", f"{len(out)} box ngoài ảnh (id {short(out)})", G["B"])
        r.check("B7", not deg, "không có box rộng/cao ≤ 0", f"{len(deg)} box suy biến (id {short(deg)})", G["B"])
        wrong, unread = [], 0
        for im in d["images"]:
            sz = jpeg_size(imgs_dir / im["file_name"]) if (imgs_dir / im["file_name"]).is_file() else None
            if sz is None:
                unread += 1
            elif sz != (im["width"], im["height"]):
                wrong.append(im["file_name"])
        r.check("B8", not wrong, "kích thước ảnh trong file nhãn khớp file ảnh thật",
                f"{len(wrong)} ảnh có width/height trong nhãn khác ảnh thật: {short(wrong)}", G["B"])
        if unread:
            r.warn("B8b", f"{unread} ảnh không đọc được header JPEG để so kích thước", G["B"])
        # đủ số nhãn: summary & CVAT
        ls = bd / "label_summary.csv"
        if ls.is_file():
            rows = read_csv(ls)
            try:
                got = {x["class"]: int(x["labels"]) for x in rows if x["class"] != "TOTAL"}
                tot = [x for x in rows if x["class"] == "TOTAL"]
                same = got == per_class
                r.check("B9", same, "label_summary.csv khớp số nhãn thật trong file nhãn",
                        f"label_summary lệch file nhãn: summary {got} / thật {per_class}", G["B"])
                r.check("B10", bool(tot) and int(tot[0]["labels"]) == labels_total and int(tot[0]["images_with_label"]) == len(d["images"]),
                        "dòng TOTAL đúng (tổng nhãn, tổng ảnh)", f"dòng TOTAL thiếu/sai (thật: {labels_total} nhãn, {len(d['images'])} ảnh)", G["B"])
            except (KeyError, ValueError):
                r.bad("B9", "label_summary.csv sai cột (cần class,labels,images_with_label)", G["B"])
        cv = WORK / "cvat_counts.csv"
        if cv.is_file():
            try:
                cvc = {x["class"]: int(x["cvat_count"]) for x in read_csv(cv) if x["class"] != "TOTAL"}
                diff = {k: (cvc.get(k, 0), per_class.get(k, 0)) for k in set(cvc) | set(per_class) if cvc.get(k, 0) != per_class.get(k, 0)}
                r.check("B11", not diff, "số nhãn theo CVAT = số nhãn trong file xuất, từng lớp",
                        f"đối soát lệch (lớp: CVAT, file xuất) {diff}", G["B"])
            except (KeyError, ValueError):
                r.bad("B11", "worklog/cvat_counts.csv sai cột (cần class,cvat_count)", G["B"])
        else:
            r.bad("B11", "thiếu submission/worklog/cvat_counts.csv (số nhãn theo CVAT, cột class,cvat_count)", G["B"])
        if cfg.get("track") == "B" and cv.is_file():
            try:
                jobs = read_csv(STARTER / "cvat_info" / "jobs.csv")
                tot = {c: sum(int(j[c]) for j in jobs) for c in cfg["classes"]}
                mine = {x["class"]: int(x["cvat_count"]) for x in read_csv(cv) if x["class"] != "TOTAL"}
                r.check("B12", tot == mine, "cvat_counts.csv = tổng các job trong cvat_info/jobs.csv",
                        f"cvat_counts.csv phải là TỔNG số nhãn các job (Info CVAT) trong jobs.csv: lệch {({k: (mine.get(k), v) for k, v in tot.items() if mine.get(k) != v})}", G["B"])
            except (KeyError, ValueError, FileNotFoundError):
                r.bad("B12", "không đối chiếu được cvat_counts.csv với cvat_info/jobs.csv", G["B"])

    at = bd / "ATTRIBUTION.csv"
    if at.is_file():
        try:
            cov = {x["new_name"] for x in read_csv(at)}
            lack = sorted(set(img_files) - cov)
            r.check("A7", not lack, "ATTRIBUTION.csv có cột new_name phủ mọi ảnh (ghi công theo tên đã đổi)",
                    f"ATTRIBUTION.csv thiếu cột new_name hoặc thiếu {len(lack)} ảnh (dùng apply_rename.py --attribution): {short(lack)}", G["A"])
        except KeyError:
            r.bad("A7", "ATTRIBUTION.csv thiếu cột new_name (dùng apply_rename.py --attribution ...)", G["A"])
    elif cfg.get("track") == "B":
        r.bad("A7", "Track B: thiếu ATTRIBUTION.csv (giấy phép CC BY yêu cầu ghi công; dùng apply_rename.py --attribution)", G["A"])
    else:
        r.warn("A7", "Track A: không có ATTRIBUTION.csv; chỉ chấp nhận nếu nguồn ảnh không đòi ghi công (nêu ở README Ghi chú)", G["A"])

    # ------------------------------------------------------------------ C
    mf = bd / "manifest.csv"
    if mf.is_file():
        rows = read_csv(mf)
        try:
            files = {x["file"]: x for x in rows}
            actual = {f"images/{n}" for n in img_files} | ({f"annotations/{ann.name}"} if ann else set())
            r.check("C1", set(files) == actual and len(rows) == len(files), f"manifest liệt kê đúng {len(actual)} file, không thiếu không thừa",
                    f"manifest lệch thư mục: thiếu {short(sorted(actual - set(files)))}; thừa {short(sorted(set(files) - actual))}", G["C"])
            badh = [f for f, x in files.items() if (bd / f).is_file() and sha256_file(bd / f) != x.get("sha256", "").lower()]
            r.check("C2", not badh, "sha256 từng file trong manifest khớp file thật",
                    f"{len(badh)} file có sha256 khác file thật (file đổi sau khi lập manifest?): {short(badh)}", G["C"])
        except KeyError:
            r.bad("C1", "manifest.csv thiếu cột file/sha256", G["C"])
    shaf = SUBMISSION / f"{bid}.sha256"
    if shaf.is_file():
        recorded = shaf.read_text(encoding="utf-8").split()[0].lower()
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / f"{bid}.zip"
            build_zip(bd, z)
            now = sha256_file(z)
        r.check("C3", now == recorded, "đóng gói lại ra đúng mã sha256 đã ghi (zip tái lập được)",
                "nội dung lô đã đổi sau khi ghi sha256: chạy lại scripts/pack_batch.py và cập nhật phiếu", G["C"])
    else:
        r.bad("C3", f"thiếu submission/{bid}.sha256 (chạy scripts/pack_batch.py)", G["C"])
        recorded = ""

    # ------------------------------------------------------------------ D
    parsed = {n: parse_img_name(n) for n in img_files}
    badn = [n for n, p in parsed.items() if not p]
    r.check("D1", not badn, "mọi tên ảnh đúng quy ước vehNN_YYYYMMDD_camX_seqNNN_NNNNNN.jpg",
            f"{len(badn)} tên sai quy ước: {short(badn)} (chạy check_names.py)", G["D"])
    good = {n: p for n, p in parsed.items() if p}
    seq_src = {}
    for n, p in good.items():
        seq_src.setdefault(p["sequence"], set()).add((p["vehicle"], p["date"], p["camera"]))
    clash = {s: sorted(v) for s, v in seq_src.items() if len(v) > 1}
    r.check("D2", not clash, f"mỗi sequence ID thuộc đúng một (xe, ngày, camera): {len(seq_src)} sequence",
            f"sequence ID dùng cho nhiều đoạn thu khác nhau (trùng mã): {clash}", G["D"])
    fr = {}
    dup = []
    for n, p in good.items():
        k = (p["sequence"], p["frame"])
        if k in fr:
            dup.append(n)
        fr[k] = n
    r.check("D3", not dup, "frame không trùng trong cùng sequence", f"frame trùng trong sequence: {short(dup)}", G["D"])
    if mf.is_file():
        try:
            bad = []
            for x in read_csv(mf):
                if x["type"] != "image":
                    continue
                p = parse_img_name(Path(x["file"]).name)
                if p and (x["scene"], x["vehicle"], x["date"], x["camera"]) != (p["sequence"], p["vehicle"], p["date"], p["camera"]):
                    bad.append(x["file"])
            r.check("D4", not bad, "cột scene/vehicle/date/camera trong manifest khớp tên file", f"manifest lệch tên file: {short(bad)}", G["D"])
        except KeyError:
            r.bad("D4", "manifest.csv thiếu cột scene/vehicle/date/camera/type", G["D"])
    tv = bd / "truyvet.csv"
    guide_set = set()
    if tv.is_file():
        rows = read_csv(tv)
        hdr_ok = rows and set(rows[0]) == {"image", "annotator", "reviewer", "guideline"}
        if r.check("D5", bool(hdr_ok), "truyvet.csv đúng cột image,annotator,reviewer,guideline", "truyvet.csv phải có đúng cột image,annotator,reviewer,guideline", G["D"]):
            im = [x["image"] for x in rows]
            r.check("D6", sorted(im) == sorted(img_files) and len(im) == len(set(im)), "truyvet.csv: mỗi ảnh đúng một dòng",
                    f"truyvet lệch images/: thiếu {short(sorted(set(img_files) - set(im)))}; thừa/lặp {short(sorted(set(im) - set(img_files)) or [i for i in im if im.count(i) > 1])}", G["D"])
            badv = [x["image"] for x in rows if not (ANNOT_RE.match(x["annotator"]) and ANNOT_RE.match(x["reviewer"]) and GUIDE_RE.match(x["guideline"]))]
            r.check("D7", not badv, "mã người (A07/Q03) và phiên bản guideline (v1.3) đúng định dạng",
                    f"{len(badv)} dòng sai định dạng mã người hoặc guideline: {short(badv)}", G["D"])
            same = [x["image"] for x in rows if x["annotator"] == x["reviewer"]]
            if same and cfg.get("allow_same_reviewer"):
                r.warn("D8", f"{len(same)} ảnh người kiểm = người gán (allow_same_reviewer=true): phải giải thích ở README Ghi chú", G["D"])
            else:
                r.check("D8", not same, "người kiểm khác người gán ở mọi ảnh", f"người kiểm trùng người gán: {short(same)}", G["D"])
            guide_set = {x["guideline"] for x in rows}
    sp = ANA / "split.csv"
    if sp.is_file():
        rows = read_csv(sp)
        by = {}
        for x in rows:
            by.setdefault(x["sequence"], set()).add(x["split"])
        lk = [s for s, v in by.items() if len(v) > 1]
        r.check("D9", not lk and {x["image"] for x in rows} == set(img_files), "split.csv chia theo sequence, không rò rỉ, đủ ảnh",
                f"split.csv rò rỉ hoặc lệch ảnh: sequence ở cả train và val {short(lk)}", G["D"])
    else:
        r.bad("D9", "thiếu submission/analysis/split.csv (chạy make_split.py --by sequence)", G["D"])

    # ------------------------------------------------------------------ E
    rd = bd / "README.txt"
    concl = {}
    if rd.is_file():
        kv = parse_readme_txt(rd)
        miss = [k for k in README_KEYS if not kv.get(k)]
        r.check("E1", not miss, "README.txt đủ 9 mục", f"README.txt thiếu mục: {miss}", G["E"])
        r.check("E2", kv.get("Lô") == bid, "README: tên lô khớp", f"README ghi Lô '{kv.get('Lô')}', cần '{bid}'", G["E"])
        ds = kv.get("Ngày nộp", "")
        okd = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", ds))
        r.check("E3", okd, "README: ngày nộp dạng YYYY-MM-DD", f"Ngày nộp '{ds}' phải dạng 2026-11-05 (một giá trị một cách viết)", G["E"])
        sc = cfg.get("submitter_code", "")
        r.check("E4", bool(ANNOT_RE.match(kv.get("Người nộp", ""))) and (not sc or sc == "S00" or kv.get("Người nộp") == sc),
                "README: mã người nộp đúng định dạng và khớp lab_config.json", f"Người nộp '{kv.get('Người nộp')}' phải dạng S34 và trùng submitter_code '{sc}' trong lab_config.json", G["E"])
        if d:
            r.check("E5", vn_int(kv.get("Số ảnh", "")) == len(d["images"]), f"README: Số ảnh = {len(d['images'])}",
                    f"README Số ảnh '{kv.get('Số ảnh')}' ≠ thật {len(d['images'])}", G["E"])
            r.check("E6", vn_int(kv.get("Số nhãn", "")) == labels_total, f"README: Số nhãn = {labels_total}",
                    f"README Số nhãn '{kv.get('Số nhãn')}' ≠ thật {labels_total}", G["E"])
        fmt = kv.get("Định dạng", "")
        r.check("E7", "COCO" in fmt and (ann is None or ann.name in fmt), "README: định dạng ghi COCO và đúng tên file nhãn",
                f"README Định dạng '{fmt}' phải ghi COCO 1.0 và đường dẫn annotations/{ann.name if ann else '...'}", G["E"])
        gl = set(re.findall(r"v\d+\.\d+", kv.get("Guideline", "")))
        if guide_set:
            r.check("E8", gl == guide_set, f"README: Guideline {sorted(gl)} khớp truyvet",
                    f"README ghi guideline {sorted(gl)} nhưng truyvet có {sorted(guide_set)}", G["E"])
        qcl = kv.get("QC", "")
        m_ = re.search(r"[-–—]\s*(Release|Hold|Rework)\s*$", qcl)
        concl["README"] = m_.group(1) if m_ else None
        r.check("E9", bool(m_), f"README: dòng QC kết thúc bằng '- {m_.group(1) if m_ else ''}'",
                "README: dòng QC phải KẾT THÚC bằng ' - Release' (hoặc Rework / Hold): kết luận cuối cùng, sau mọi vòng QC", G["E"])
    qr = bd / "qc_report.txt"
    if qr.is_file():
        t = qr.read_text(encoding="utf-8")
        kv = parse_kv(qr)
        c = [x for x in CONCL if kv.get("Kết luận", "").startswith(x)]
        concl["qc_report"] = c[0] if c else None
        r.check("E10", bool(c), f"qc_report: Kết luận {c[0] if c else ''}", "qc_report.txt thiếu dòng 'Kết luận: Release|Hold|Rework'", G["E"])
        fr_ = re.findall(r"(\d+)\s*/\s*(\d+)", t)
        r.check("E11", bool(fr_), "qc_report: có mẫu số (a/b)", "qc_report.txt phải ghi tỉ lệ kèm mẫu số dạng 39/40", G["E"])
        rate_lines = [ln for ln in t.splitlines() if ln.strip().startswith("Tỉ lệ ảnh đạt")]
        if rate_lines and c:
            m = re.findall(r"(\d+)\s*/\s*(\d+)", rate_lines[-1])
            if m and d and int(m[0][1]) > len(d["images"]):
                r.bad("E12", f"mẫu số {m[0][1]} lớn hơn số ảnh của lô ({len(d['images'])})", G["E"])
            elif m:
                a_, b_ = map(int, m[0])
                rate = a_ / b_ if b_ else 0
                if c[0] == "Release" and rate < 0.98:
                    r.bad("E12", f"Release nhưng tỉ lệ đạt cuối cùng {a_}/{b_} = {rate:.1%} < 98% (ngưỡng Day 7)", G["E"])
                else:
                    r.ok("E12", f"kết luận {c[0]} hợp với tỉ lệ đạt cuối {a_}/{b_} = {rate:.1%}", G["E"])
            else:
                r.warn("E12", "dòng 'Tỉ lệ ảnh đạt' cuối không có phân số a/b: không đối chiếu được với ngưỡng", G["E"])
        else:
            r.warn("E12", "không có dòng 'Tỉ lệ ảnh đạt ...' để đối chiếu kết luận với ngưỡng", G["E"])
    # ------------------------------------------------------------------ F
    ph = SUBMISSION / "phieu_ban_giao.md"
    if ph.is_file():
        kv = parse_kv(ph)
        miss = [k for k in PHIEU_KEYS if not kv.get(k)]
        r.check("F1", not miss, "phiếu bàn giao đủ 8 dòng", f"phiếu thiếu dòng: {miss}", G["F"])
        r.check("F2", kv.get("Tên lô") == bid, "phiếu: tên lô khớp", f"phiếu ghi '{kv.get('Tên lô')}', cần '{bid}'", G["F"])
        if d:
            r.check("F3", vn_int(kv.get("Số ảnh", "")) == len(d["images"]) and vn_int(kv.get("Số nhãn", "")) == labels_total,
                    "phiếu: số ảnh, số nhãn khớp thật", f"phiếu Số ảnh/Số nhãn lệch thật ({len(d['images'])}/{labels_total})", G["F"])
        r.check("F4", bool(recorded) and recorded in kv.get("SHA-256 zip", "").lower(), "phiếu: SHA-256 zip khớp .sha256",
                "phiếu: SHA-256 zip trống hoặc khác submission/<lô>.sha256", G["F"])
        c = [x for x in CONCL if kv.get("Kết luận", "").startswith(x)]
        concl["phieu"] = c[0] if c else None
        txt = ph.read_text(encoding="utf-8")
        boxes = re.findall(r"^\s*[-*]\s*\[( |x|X)\]", txt, flags=re.M)
        r.check("F5", len(boxes) >= 5 and all(b.lower() == "x" for b in boxes), f"checklist {len(boxes)} mục đã tích đủ",
                f"checklist cuối phiếu cần ≥ 5 mục và tích hết (đang {sum(b.lower()=='x' for b in boxes)}/{len(boxes)}); chưa đủ thì chưa nộp", G["F"])
    else:
        r.bad("F1", "thiếu submission/phieu_ban_giao.md", G["F"])
    vals = {v for v in concl.values() if v}
    if len(concl) >= 2:
        r.check("F6", len(vals) == 1 and None not in concl.values(), f"kết luận nhất quán ở README, qc_report, phiếu: {vals}",
                f"kết luận không nhất quán giữa các nơi: {concl}", G["F"])
    sec = SUBMISSION / "security.md"
    if sec.is_file():
        t = sec.read_text(encoding="utf-8")
        parts = re.split(r"^##\s+", t, flags=re.M)[1:]

        def body(p_):
            lines = p_.split("\n")[1:]
            return "".join(re.sub(r"\s+", "", ln) for ln in lines if not ln.lstrip().startswith(">") and not re.fullmatch(r"[\s|:-]*", ln))
        filled = [p for p in parts if len(body(p)) >= 80]
        r.check("F7", len(parts) >= 7 and len(filled) >= 7, f"security.md: {len(filled)}/{len(parts)} mục đã trả lời",
                f"security.md cần ≥ 7 mục (## ...) mỗi mục có nội dung (đang {len(filled)}/{len(parts)} mục có nội dung)", G["F"])
        face = [p for p in parts if "khuôn mặt" in p.split("\n")[0].lower()]
        r.check("F8", bool(face) and "Hold" in face[0] and "người phụ trách" in face[0].lower(), "security.md: ca khuôn mặt kết luận Hold + báo người phụ trách",
                "security.md: mục về khuôn mặt phải kết luận Hold và nêu báo 'người phụ trách'", G["F"])
    else:
        r.bad("F7", "thiếu submission/security.md", G["F"])

    # ------------------------------------------------------------------ G
    must = {"kiem_lo.py": 300, "prompts.md": 80, "bug_ticket.md": 80, "mutation_test.md": 80, "rename_map.csv": 30,
            "seq_remap.csv": 5, "cvat_counts.csv": 10, "drills.md": 200}
    for fn, mn in must.items():
        p = WORK / fn
        r.check(f"G-{fn}", p.is_file() and p.stat().st_size >= mn, f"worklog/{fn} có",
                f"thiếu hoặc quá ngắn: submission/worklog/{fn}", G["G"])
    reps = list(WORK.glob("check_report*.txt")) if WORK.is_dir() else []
    r.check("G-report", bool(reps), f"có báo cáo kiểm export: {short(p.name for p in reps)}", "thiếu submission/worklog/check_report_*.txt (output của kiem_lo.py)", G["G"])
    kl = WORK / "kiem_lo.py"
    if kl.is_file():
        src = kl.read_text(encoding="utf-8")
        try:
            mods = set()
            for n_ in ast.walk(ast.parse(src)):
                if isinstance(n_, ast.Import):
                    mods |= {a_.name.split(".")[0] for a_ in n_.names}
                elif isinstance(n_, ast.ImportFrom) and n_.module:
                    mods.add(n_.module.split(".")[0])
            own = not (mods & {"common", "scripts", "check_batch", "apply_rename"}) and "sys.path" not in src.replace(" ", "")
            r.check("G-own", own, "kiem_lo.py tự viết (không import từ scripts/)", "kiem_lo.py không được import từ scripts/ hay sửa sys.path: phải tự viết", G["G"])
        except SyntaxError as e:
            r.bad("G-own", f"kiem_lo.py lỗi cú pháp: {e}", G["G"])
        harness(r, cfg, kl, G["G"])
    ia = ANA / "impact_analysis.md"
    if ia.is_file():
        t = ia.read_text(encoding="utf-8")
        nnn = BATCH_RE.match(bid).group(1)
        r.check("G-v2", f"lo_{nnn}_v2" in t, f"impact_analysis đặt tên lô sửa lo_{nnn}_v2", f"impact_analysis.md phải nêu tên lô sửa lo_{nnn}_v2 (không ghi đè v1)", G["G"])
        names = set(re.findall(r"veh\d{2}_\d{8}_cam[A-Z]_seq\d{3}_\d{6}\.jpg", t))
        r.check("G-ia-img", bool(names) and names <= set(img_files), f"impact_analysis liệt kê {len(names)} ảnh, đều thuộc lô",
                "impact_analysis.md phải liệt kê tên ảnh (đúng tên trong lô) cần mở lại", G["G"])
    else:
        r.bad("G-ia", "thiếu submission/analysis/impact_analysis.md", G["G"])
    for fn in ["submission/individual_note.md"]:
        r.check("G-note", (ROOT / fn).is_file(), "có individual_note.md", f"thiếu {fn}", G["G"])
    # placeholder còn sót
    scan = [bd / n for n in ("README.txt", "qc_report.txt")] + [SUBMISSION / "phieu_ban_giao.md", SUBMISSION / "security.md",
            ANA / "impact_analysis.md", SUBMISSION / "individual_note.md", WORK / "bug_ticket.md", WORK / "mutation_test.md", WORK / "prompts.md", WORK / "drills.md"]
    left = [p.name for p in scan if p.is_file() and "<<" in p.read_text(encoding="utf-8")]
    r.check("G-ph", not left, "không còn chỗ <<...>> chưa điền", f"còn <<...>> chưa điền trong: {short(left)}", G["G"])
    finish(r, args)


def export_paths(cfg):
    """(file nhãn export_1, export_2, thư mục ảnh nguồn) theo track; None nếu không có."""
    if cfg.get("track") == "B":
        e1 = STARTER / "cvat_export_1" / "annotations" / "instances_default.json"
        e2 = STARTER / "cvat_export_2_reexport" / "annotations" / "instances_default.json"
        return e1, e2, STARTER / "images"
    w = WORK
    e1, e2 = w / "export_1" / "annotations" / "instances_default.json", w / "export_2" / "annotations" / "instances_default.json"
    imgs = Path(cfg["images_dir"]) if cfg.get("images_dir") else None
    return e1, e2, (ROOT / imgs if imgs and not imgs.is_absolute() else imgs)


def run_kiem(kl: Path, labels: Path, imgs: Path, classes, cv: Path, out: Path):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    cmd = [sys.executable, str(kl), str(labels), str(imgs), "--classes", *classes, "--cvat-counts", str(cv), "--out", str(out)]
    return subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60, encoding="utf-8", errors="replace")


def harness(r: R, cfg, kl: Path, g: str) -> None:
    """Chạy lại kiem_lo.py của học viên: có chạy được không, export_1 KHÔNG ĐẠT, export_2 ĐẠT, báo cáo đã nộp đúng là output thật."""
    e1, e2, imgs = export_paths(cfg)
    cv = WORK / "cvat_counts.csv"
    if not (e1.is_file() and imgs and imgs.is_dir() and cv.is_file()):
        r.warn("G-run", "không tìm được export_1/thư mục ảnh/cvat_counts để chạy lại kiem_lo.py (Track A: đặt export ở worklog/export_1|2 và đặt images_dir trong lab_config.json)", g)
        return
    with tempfile.TemporaryDirectory() as td:
        o1 = Path(td) / "o1.txt"
        try:
            p1 = run_kiem(kl, e1, imgs, cfg["classes"], cv, o1)
        except (subprocess.TimeoutExpired, OSError) as e:
            r.bad("G-run1", f"kiem_lo.py không chạy được: {e}", g)
            return
        if not o1.is_file():
            r.bad("G-run1", f"kiem_lo.py phải hỗ trợ --out <file> (ghi báo cáo UTF-8); stderr: {p1.stderr.strip()[-200:]}", g)
            return
        want_fail = cfg.get("track") == "B" or True
        r.check("G-run1", p1.returncode == 1, "kiem_lo.py trên export_1: thoát mã 1 (KHÔNG ĐẠT)",
                f"kiem_lo.py trên export_1 phải thoát mã 1 vì file có lỗi (đang mã {p1.returncode})", g)
        rep = WORK / "check_report_export1.txt"
        norm = lambda x: sorted(re.findall(r"[^\s,\[\]{}()]+", x))  # bỏ qua thứ tự (script dùng set có thể in thứ tự khác nhau mỗi lần chạy)
        live = norm(o1.read_text(encoding="utf-8", errors="replace"))
        if rep.is_file():
            got = norm(rep.read_text(encoding="utf-8-sig", errors="replace"))
            r.check("G-rep1", got == live, "check_report_export1.txt trùng output thật của kiem_lo.py", "check_report_export1.txt khác output chạy lại kiem_lo.py: báo cáo phải là output thật, không gõ tay", g)
        # bug_ticket phải nêu từng lỗi mà script thấy (tính từ export_1, không cần đáp án)
        bt = WORK / "bug_ticket.md"
        if bt.is_file():
            t = bt.read_text(encoding="utf-8")
            d1 = json.loads(e1.read_text(encoding="utf-8"))
            cn = {c["id"]: c["name"] for c in d1["categories"]}
            need = [repr(n) for n in cn.values() if n not in cfg["classes"]]
            iid = {i["id"]: i for i in d1["images"]}
            ids = []
            for a_ in d1["annotations"]:
                x, y, w, h = a_["bbox"]
                im = iid.get(a_["image_id"])
                if im and (w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > im["width"] or y + h > im["height"]):
                    ids.append(a_["id"])
            miss_img = sorted(n for n in (p_.name for p_ in list_files(imgs)) if n not in {i["file_name"] for i in d1["images"]})
            lack = [n for n in need if n not in t and n.strip("'") not in t] + [str(i) for i in ids if not re.search(rf"\b{i}\b", t)] + [m_ for m_ in miss_img if m_ not in t]
            r.check("G-ticket", not lack, f"bug_ticket.md nêu đủ {len(need)} tên lớp sai, {len(ids)} nhãn box lỗi, {len(miss_img)} ảnh thiếu",
                    f"bug_ticket.md chưa nêu cụ thể: {short(lack, 6)} (tên lớp sai, id nhãn box lỗi, tên ảnh thiếu: đúng như script báo ở export_1)", g)
        if e2.is_file():
            o2 = Path(td) / "o2.txt"
            p2 = run_kiem(kl, e2, imgs, cfg["classes"], cv, o2)
            r.check("G-run2", p2.returncode == 0, "kiem_lo.py trên export_2: ĐẠT (mã 0)", f"kiem_lo.py trên export_2 phải ĐẠT (mã 0), đang mã {p2.returncode}", g)
        else:
            r.warn("G-run2", "không có export_2 để chạy lại", g)
    # fixture mutation: kiem_lo phải thoát 1 trên một vài lỗi cài tạm thời
    d0 = json.loads(e1.read_text(encoding="utf-8"))
    mut = [("tên lớp thừa dấu cách", lambda x: x["categories"][0].__setitem__("name", x["categories"][0]["name"] + " ")),
           ("box ngoài ảnh", lambda x: x["annotations"][0].__setitem__("bbox", [x["images"][0]["width"] + 5, 0, 10, 10])),
           ("xoá một ảnh", lambda x: x["images"].pop())]
    d2 = json.loads(e2.read_text(encoding="utf-8")) if e2.is_file() else None
    if d2:
        caught = 0
        with tempfile.TemporaryDirectory() as td:
            for i, (nm, f) in enumerate(mut):
                x = json.loads(json.dumps(d2))
                f(x)
                lp = Path(td) / f"m{i}.json"
                lp.write_text(json.dumps(x), encoding="utf-8")
                pr = run_kiem(kl, lp, imgs, cfg["classes"], cv, Path(td) / f"m{i}.txt")
                caught += pr.returncode == 1
        r.check("G-mut", caught == len(mut), f"kiem_lo.py bắt được {caught}/{len(mut)} lỗi cài ẩn do bộ kiểm tạo",
                f"kiem_lo.py chỉ bắt {caught}/{len(mut)} lỗi cài ẩn (tên lớp thừa dấu cách, box ngoài ảnh, thiếu ảnh): script có bỏ sót", g)


def finish(r: R, args) -> None:
    cur = None
    for x in r.rows:
        if x["group"] != cur:
            cur = x["group"]
            print(f"\n{cur}")
        print(f"  [{x['status']}] {x['id']:<9} {x['msg']}")
    n = {s: sum(1 for x in r.rows if x["status"] == s) for s in ("PASS", "WARN", "FAIL")}
    print(f"\nTổng: {n['PASS']} PASS, {n['WARN']} WARN, {n['FAIL']} FAIL")
    print("=> " + ("ĐỦ ĐIỀU KIỆN VỀ ĐỊNH DẠNG. Nhớ: PASS không có nghĩa nhãn đúng; QC của người vẫn là bắt buộc." if not n["FAIL"]
                   else "CHƯA NỘP ĐƯỢC: sửa các dòng FAIL."))
    if args.json:
        Path(args.json).write_text(json.dumps(r.rows, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.exit(1 if n["FAIL"] else 0)


if __name__ == "__main__":
    main()
