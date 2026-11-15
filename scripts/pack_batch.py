"""Đóng gói thư mục lô thành .zip có thể tái lập (cùng nội dung -> cùng sha256) và ghi file .sha256.

    python scripts/pack_batch.py

Ghi: submission/<batch_id>.zip (KHÔNG commit, đã nằm trong .gitignore) và submission/<batch_id>.sha256 (commit file này).
Zip dùng chế độ STORED, thứ tự file cố định, mốc thời gian cố định để mã băm không phụ thuộc máy / thời điểm.
Chỉ chạy sau khi mọi file trong lô đã chốt: sửa bất kỳ file nào thì phải đóng gói và ghi hash lại.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import HIDDEN, SUBMISSION, batch_dir, die, load_config, sha256_file  # noqa: E402

FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def build_zip(bd: Path, out: Path) -> None:
    files = sorted((p for p in bd.rglob("*") if p.is_file() and not p.name.startswith(".") and p.name.lower() not in HIDDEN),
                   key=lambda p: p.relative_to(bd).as_posix())
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED) as z:
        for p in files:
            arc = f"{bd.name}/{p.relative_to(bd).as_posix()}"
            zi = zipfile.ZipInfo(arc, date_time=FIXED_TIME)
            zi.compress_type = zipfile.ZIP_STORED
            zi.external_attr = 0o644 << 16
            zi.create_system = 3  # cố định, không phụ thuộc hệ điều hành
            z.writestr(zi, p.read_bytes())


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    cfg = load_config()
    bd = batch_dir(cfg)
    if not bd.is_dir():
        die(f"Không thấy thư mục lô {bd}.")
    out = SUBMISSION / f"{bd.name}.zip"
    build_zip(bd, out)
    h = sha256_file(out)
    (SUBMISSION / f"{bd.name}.sha256").write_text(f"{h}  {out.name}\n", encoding="utf-8")
    print(f"Đã tạo {out}  ({out.stat().st_size:,} byte)")
    print(f"sha256: {h}")
    print(f"Ghi vào phiếu bàn giao; đã lưu {SUBMISSION / (bd.name + '.sha256')}")


if __name__ == "__main__":
    main()
