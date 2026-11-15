"""Sinh label_summary.csv: số nhãn và số ảnh có nhãn THEO TỪNG LỚP, đọc từ file nhãn trong lô.

    python scripts/build_label_summary.py

Cột: class,labels,images_with_label. Dòng cuối TOTAL: tổng nhãn, tổng số ảnh của lô.
Một ảnh có thể chứa nhiều lớp nên cột images_with_label KHÔNG cộng lại bằng tổng số ảnh.
Lớp có tên lạ vẫn được liệt kê đúng như trong file: nếu thấy tên lạ, quay lại sửa nhãn, đừng sửa summary.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import batch_dir, die, find_annotation_file, load_coco, load_config, write_csv  # noqa: E402


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    cfg = load_config()
    bd = batch_dir(cfg)
    ap = find_annotation_file(bd)
    if not ap:
        die(f"Không thấy file nhãn trong {bd / 'annotations'}.")
    d = load_coco(ap)
    name = {c["id"]: c["name"] for c in d["categories"]}
    labels, imgs = {}, {}
    for a in d["annotations"]:
        n = name.get(a["category_id"], f"?id{a['category_id']}")
        labels[n] = labels.get(n, 0) + 1
        imgs.setdefault(n, set()).add(a["image_id"])
    order = [c for c in cfg["classes"] if c in labels] + sorted(n for n in labels if n not in cfg["classes"])
    rows = [[n, labels[n], len(imgs[n])] for n in order]
    rows.append(["TOTAL", sum(labels.values()), len(d["images"])])
    write_csv(bd / "label_summary.csv", ["class", "labels", "images_with_label"], rows)
    print(f"Đã ghi {bd / 'label_summary.csv'}")
    for r in rows:
        print("  ", *r)


if __name__ == "__main__":
    main()
