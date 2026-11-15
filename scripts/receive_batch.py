"""Đóng vai TEAM AI nhận lô: chỉ có file .zip và mã sha256, KHÔNG có bạn ngồi cạnh để hỏi.

    python scripts/receive_batch.py submission/lo_234_v1.zip submission/lo_234_v1.sha256
    python scripts/receive_batch.py <zip> <mã 64 ký tự>

Các bước (giống team AI thật): so hash -> giải nén vào thư mục tạm -> đọc README.txt -> nạp file nhãn ->
đối chiếu số lượng với label_summary -> so hash từng file với manifest -> in danh sách câu hỏi còn phải hỏi lại.
Bài làm tốt: phần "CÂU HỎI CÒN PHẢI HỎI LẠI" trống.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import parse_readme_txt, read_csv, sha256_file, vn_int  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("zip")
    ap.add_argument("sha")
    a = ap.parse_args()
    z = Path(a.zip)
    if not z.is_file():
        print(f"Không thấy {z}. Tạo bằng scripts/pack_batch.py.")
        sys.exit(2)
    want = Path(a.sha).read_text(encoding="utf-8").split()[0] if Path(a.sha).is_file() else a.sha.strip()
    got = sha256_file(z)
    questions = []
    print(f"sha256 nhận được : {got}\nsha256 người gửi : {want}")
    if got.lower() != want.lower():
        print("=> KHÁC: dừng, không dùng lô này, yêu cầu gửi lại.")
        sys.exit(1)
    print("=> KHỚP\n")
    with tempfile.TemporaryDirectory() as td:
        try:
            with zipfile.ZipFile(z) as zf:
                zf.extractall(td)
        except zipfile.BadZipFile:
            print("Giải nén lỗi: zip hỏng.")
            sys.exit(1)
        roots = [p for p in Path(td).iterdir() if p.is_dir()]
        if len(roots) != 1:
            questions.append("zip phải chứa đúng MỘT thư mục lô ở gốc")
            roots = roots or [Path(td)]
        bd = roots[0]
        print(f"Thư mục lô: {bd.name}")
        if not (bd / "README.txt").is_file():
            questions.append("không có README.txt: không biết lô gồm gì, gán theo guideline nào")
        else:
            kv = parse_readme_txt(bd / "README.txt")
            for k in ("Lô", "Ngày nộp", "Người nộp", "Số ảnh", "Số nhãn", "Guideline", "Định dạng", "QC"):
                if not kv.get(k):
                    questions.append(f"README.txt thiếu mục '{k}'")
            print("README:", {k: kv.get(k) for k in ("Lô", "Số ảnh", "Số nhãn", "Guideline", "QC")})
        ann = sorted((bd / "annotations").glob("*.json"))
        d = None
        if len(ann) != 1:
            questions.append(f"annotations/ có {len(ann)} file nhãn, không biết dùng file nào")
        else:
            try:
                d = json.loads(ann[0].read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                questions.append(f"file nhãn không đọc được: {e}")
        if d:
            name = {c["id"]: c["name"] for c in d["categories"]}
            cnt = {}
            for x in d["annotations"]:
                cnt[name.get(x["category_id"], "?")] = cnt.get(name.get(x["category_id"], "?"), 0) + 1
            print(f"Nạp được: {len(d['images'])} ảnh, {len(d['annotations'])} nhãn, lớp: {cnt}")
            if len(name) != len(set(name.values())) or any(n != n.strip() or n != n.lower() for n in name.values()):
                questions.append(f"tên lớp đáng ngờ (hoa/thường, dấu cách): {[repr(n) for n in name.values()]}")
            ls = bd / "label_summary.csv"
            if ls.is_file():
                s = {x["class"]: int(x["labels"]) for x in read_csv(ls) if x["class"] != "TOTAL"}
                if s != cnt:
                    questions.append(f"label_summary ({s}) lệch số nhãn thật ({cnt}): mất nhãn?")
            else:
                questions.append("không có label_summary.csv để đối chiếu mất nhãn")
            if (bd / "README.txt").is_file():
                kv = parse_readme_txt(bd / "README.txt")
                if vn_int(kv.get("Số ảnh", "")) != len(d["images"]) or vn_int(kv.get("Số nhãn", "")) != len(d["annotations"]):
                    questions.append("README ghi số ảnh/số nhãn khác file nhãn")
            files = {p.name for p in (bd / "images").glob("*.jpg")} if (bd / "images").is_dir() else set()
            if files != {i["file_name"] for i in d["images"]}:
                questions.append("danh sách ảnh trong images/ khác file nhãn")
        mf = bd / "manifest.csv"
        if mf.is_file():
            bad = [x["file"] for x in read_csv(mf) if not (bd / x["file"]).is_file() or sha256_file(bd / x["file"]) != x["sha256"].lower()]
            print(f"Manifest: {len(read_csv(mf))} dòng, sai hash/thiếu: {len(bad)}")
            if bad:
                questions.append(f"{len(bad)} file lệch manifest: {bad[:3]}")
        else:
            questions.append("không có manifest.csv")
        for n, why in (("truyvet.csv", "không truy được ai gán/kiểm, guideline nào"), ("qc_report.txt", "không biết độ tin cậy của lô")):
            if not (bd / n).is_file():
                questions.append(f"thiếu {n}: {why}")
    print("\nCÂU HỎI CÒN PHẢI HỎI LẠI NGƯỜI GỬI:")
    for q in questions:
        print("  -", q)
    if not questions:
        print("  (không có) -> dùng ngay được, đúng mục tiêu bàn giao.")
    sys.exit(1 if questions else 0)


if __name__ == "__main__":
    main()
