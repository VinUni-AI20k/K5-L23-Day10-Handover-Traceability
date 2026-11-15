"""Kiểm tên file ảnh theo quy ước lô bàn giao và giải thích TỪNG chỗ sai.

    python scripts/check_names.py veh03_20261105_camF_seq017_000001.jpg veh03_051125_camF_seq017_000003.jpg
    python scripts/check_names.py --dir submission/lo_234_v1/images

Mẫu: vehNN_YYYYMMDD_camX_seqNNN_NNNNNN.jpg   (X thuộc F, B, L, R)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import IMG_RE, parse_img_name  # noqa: E402

PARTS = r"^(veh\d{2})_(\d{8})_(cam[FBLR])_(seq\d{3})_(\d{6})\.jpg$"


def explain(name: str) -> str:
    if parse_img_name(name):
        return "đúng"
    toks = name[:-4].split("_") if name.lower().endswith(".jpg") else name.split("_")
    why = []
    if not name.endswith(".jpg"):
        why.append("đuôi phải là .jpg (chữ thường)")
    if len(toks) != 5:
        return f"phải có 5 phần ngăn bởi '_' (xe, ngày, camera, sequence, frame), đang có {len(toks)}: thiếu hoặc thừa một phần"
    if not toks or not re.fullmatch(r"veh\d{2}", toks[0]):
        why.append("phần xe phải là vehNN (vd veh03)")
    if len(toks) > 1 and not re.fullmatch(r"\d{8}", toks[1]):
        why.append("ngày phải là YYYYMMDD (8 chữ số)")
    elif len(toks) > 1:
        try:
            import datetime
            datetime.date(int(toks[1][:4]), int(toks[1][4:6]), int(toks[1][6:]))
        except ValueError:
            why.append("ngày không tồn tại trên lịch")
    if len(toks) > 2 and not re.fullmatch(r"cam[FBLR]", toks[2]):
        why.append("camera phải là camF / camB / camL / camR")
    if len(toks) > 3 and not re.fullmatch(r"seq\d{3}", toks[3]):
        why.append("sequence phải là seqNNN (3 chữ số, vd seq017)")
    if len(toks) > 4 and not re.fullmatch(r"\d{6}", toks[4]):
        why.append("frame phải là 6 chữ số (vd 000123)")
    return "; ".join(why) or "sai định dạng"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*")
    ap.add_argument("--dir", help="kiểm mọi file ảnh trong thư mục (bỏ file ẩn)")
    a = ap.parse_args()
    names = list(a.names)
    if a.dir:
        from common import list_files
        names += [p.name for p in list_files(Path(a.dir)) if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    if not names:
        ap.error("cho ít nhất một tên file hoặc --dir")
    bad = 0
    for n in names:
        r = explain(n)
        ok = r == "đúng"
        bad += not ok
        print(f"{'OK  ' if ok else 'SAI '} {n}" + ("" if ok else f"\n       -> {r}"))
    print(f"\n{len(names) - bad}/{len(names)} tên đúng quy ước")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
