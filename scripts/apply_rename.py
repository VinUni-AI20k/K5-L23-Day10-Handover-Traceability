"""Đổi tên ảnh theo bảng rename_map.csv: chép ảnh vào lô VÀ sửa `file_name` trong file nhãn COCO cho khớp.

rename_map.csv có đúng hai cột:  old_name,new_name   (một dòng mỗi ảnh)

    python scripts/apply_rename.py --map submission/worklog/rename_map.csv \
        --src-images data/starter/images \
        --src-annotations data/starter/cvat_export_2_reexport/annotations/instances_default.json \
        --attribution data/starter/ATTRIBUTION.csv
(Trên PowerShell gõ trên một dòng, bỏ dấu \\.)

Kết quả (trong submission/<batch_id>/): images/<tên mới>.jpg và annotations/instances_v1.json.
Không sửa file gốc. Vì sao phải sửa cả file nhãn: nếu chỉ đổi tên ảnh, file nhãn vẫn trỏ tên cũ và team AI không ghép được ảnh với nhãn.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import batch_dir, die, load_config, parse_img_name, read_csv  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", required=True)
    ap.add_argument("--src-images", required=True)
    ap.add_argument("--src-annotations", required=True)
    ap.add_argument("--annotation-name", default="instances_v1.json")
    ap.add_argument("--attribution", help="ATTRIBUTION.csv gốc (cột file = tên cũ): ghi bản có thêm cột new_name vào lô")
    a = ap.parse_args()

    cfg = load_config()
    bd = batch_dir(cfg)
    rows = read_csv(Path(a.map))
    if not rows or not {"old_name", "new_name"} <= set(rows[0]):
        die("rename_map.csv phải có cột old_name,new_name, ngăn bằng dấu phẩy (Excel vi-VN hay lưu dấu chấm phẩy ';': hãy lưu "
            "'CSV UTF-8 (Comma delimited)').")
    olds = [r["old_name"].strip() for r in rows]
    news = [r["new_name"].strip() for r in rows]
    if len(set(olds)) != len(olds):
        die("old_name bị lặp trong rename_map.csv.")
    if len(set(news)) != len(news):
        dup = sorted({n for n in news if news.count(n) > 1})
        die(f"new_name bị lặp (hai ảnh trùng tên): {dup}")
    bad = [n for n in news if not parse_img_name(n)]
    if bad:
        die(f"{len(bad)} tên mới sai quy ước, ví dụ {bad[:3]}. Chạy scripts/check_names.py để xem lý do.")

    src = Path(a.src_images)
    miss = [o for o in olds if not (src / o).is_file()]
    if miss:
        die(f"Không thấy {len(miss)} ảnh nguồn trong {src}: {miss[:5]}")

    d = json.loads(Path(a.src_annotations).read_text(encoding="utf-8"))
    mp = dict(zip(olds, news))
    unmapped = [i["file_name"] for i in d["images"] if i["file_name"] not in mp]
    if unmapped:
        die(f"Ảnh trong file nhãn nhưng không có trong rename_map.csv: {unmapped[:5]}")

    if (bd / "images").is_dir():
        for old in (bd / "images").iterdir():  # tránh để lại ảnh tên cũ từ lần chạy trước
            if old.is_file():
                old.unlink()
    (bd / "images").mkdir(parents=True, exist_ok=True)
    (bd / "annotations").mkdir(parents=True, exist_ok=True)
    for o, n in mp.items():
        shutil.copy2(src / o, bd / "images" / n)
    for im in d["images"]:
        im["file_name"] = mp[im["file_name"]]
    (bd / "annotations" / a.annotation_name).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    if a.attribution:
        import csv, re as _re
        src_rows = read_csv(Path(a.attribution))
        clean = lambda v: _re.sub(r"\s+", " ", (v or "").replace("\xa0", " ")).strip()
        out = []
        for r_ in src_rows:
            if r_["file"] in mp:
                out.append({"new_name": mp[r_["file"]], **{k: clean(v) for k, v in r_.items()}})
        with open(bd / "ATTRIBUTION.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(out)
        print(f"Đã ghi {bd / 'ATTRIBUTION.csv'} ({len(out)} dòng, thêm cột new_name)")
    print(f"Đã chép {len(mp)} ảnh vào {bd / 'images'} và ghi {bd / 'annotations' / a.annotation_name}")


if __name__ == "__main__":
    main()
