"""Truy vết ngược: từ một báo lỗi, khoanh vùng ảnh cần mở lại và người cần báo, dựa trên truyvet.csv.

    python scripts/trace_query.py --guideline vX.Y
    python scripts/trace_query.py --guideline vX.Y --sequence seqAAA seqBBB --has-class <tên lớp>
    python scripts/trace_query.py --annotator <mã người gán>

Đọc submission/<batch_id>/truyvet.csv (cột: image,annotator,reviewer,guideline) và, nếu có --has-class, file nhãn của lô.
Các bộ lọc ghép bằng AND. Kết quả in ra màn hình; bạn tự chép vào impact_analysis.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import batch_dir, die, find_annotation_file, load_coco, load_config, parse_img_name, read_csv  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--guideline")
    ap.add_argument("--annotator")
    ap.add_argument("--reviewer")
    ap.add_argument("--sequence", nargs="+")
    ap.add_argument("--has-class")
    a = ap.parse_args()

    bd = batch_dir(load_config())
    tp = bd / "truyvet.csv"
    if not tp.exists():
        die(f"Chưa có {tp}.")
    rows = read_csv(tp)
    if a.guideline:
        rows = [r for r in rows if r["guideline"] == a.guideline]
    if a.annotator:
        rows = [r for r in rows if r["annotator"] == a.annotator]
    if a.reviewer:
        rows = [r for r in rows if r["reviewer"] == a.reviewer]
    if a.sequence:
        rows = [r for r in rows if (parse_img_name(r["image"]) or {}).get("sequence") in a.sequence]
    if a.has_class:
        ap_ = find_annotation_file(bd)
        if not ap_:
            die("Không thấy file nhãn để lọc theo lớp.")
        d = load_coco(ap_)
        cid = {c["name"]: c["id"] for c in d["categories"]}.get(a.has_class)
        iid = {i["file_name"]: i["id"] for i in d["images"]}
        has = {x["image_id"] for x in d["annotations"] if x["category_id"] == cid}
        rows = [r for r in rows if iid.get(r["image"]) in has]
    if not rows:
        allr = read_csv(tp)
        print("KHÔNG có ảnh nào khớp. Giá trị hợp lệ trong truyvet.csv:")
        print("  guideline:", sorted({r["guideline"] for r in allr}), " annotator:", sorted({r["annotator"] for r in allr}),
              " reviewer:", sorted({r["reviewer"] for r in allr}))
        print("  sequence:", sorted({(parse_img_name(r["image"]) or {}).get("sequence", "?") for r in allr}), " lớp:", load_config()["classes"])
        sys.exit(1)
    print(f"{len(rows)} ảnh khớp bộ lọc")
    for r in rows:
        print(f"  {r['image']}  gán: {r['annotator']}  kiểm: {r['reviewer']}  guideline: {r['guideline']}")
    print("Người gán cần báo:", ", ".join(sorted({r['annotator'] for r in rows})) or "-")
    print("Người kiểm cần báo:", ", ".join(sorted({r['reviewer'] for r in rows})) or "-")


if __name__ == "__main__":
    main()
