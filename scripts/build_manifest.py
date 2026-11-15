"""Sinh manifest.csv từ thư mục lô: mỗi file ảnh / file nhãn một dòng, kèm sha256.

    python scripts/build_manifest.py

Đọc submission/<batch_id>/images và annotations. Cột scene/vehicle/date/camera lấy TỪ TÊN FILE:
tên sai quy ước thì để trống và script cảnh báo (sửa tên, đừng sửa tay manifest).
Ghi: submission/<batch_id>/manifest.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import batch_dir, die, list_files, load_config, parse_img_name, sha256_file, write_csv  # noqa: E402


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    cfg = load_config()
    bd = batch_dir(cfg)
    if not (bd / "images").is_dir():
        die(f"Chưa có {bd / 'images'}. Chạy apply_rename.py trước.")
    rows, warn = [], 0
    for p in list_files(bd / "images"):
        m = parse_img_name(p.name)
        if not m:
            warn += 1
            print(f"CẢNH BÁO: tên sai quy ước: {p.name}")
        m = m or {}
        rows.append([f"images/{p.name}", "image", m.get("sequence", ""), m.get("vehicle", ""), m.get("date", ""),
                     m.get("camera", ""), p.stat().st_size, sha256_file(p)])
    if (bd / "annotations").is_dir():
        for p in list_files(bd / "annotations"):
            if True:
                rows.append([f"annotations/{p.name}", "annotation", "", "", "", "", p.stat().st_size, sha256_file(p)])
    write_csv(bd / "manifest.csv", ["file", "type", "scene", "vehicle", "date", "camera", "bytes", "sha256"], rows)
    print(f"Đã ghi {bd / 'manifest.csv'}: {len(rows)} dòng ({warn} cảnh báo tên)")


if __name__ == "__main__":
    main()
