"""Chia train / val để THẤY rò rỉ dữ liệu: chia theo frame (sai) và chia theo sequence (đúng).

    python scripts/make_split.py --by frame      --seed 1     # cách sai, sẽ báo sequence bị rò
    python scripts/make_split.py --by sequence   --seed 1     # cách đúng
    python scripts/make_split.py --check submission/analysis/split.csv   # chỉ kiểm một file split có sẵn

Ghi submission/analysis/split.csv (cột: image,sequence,split). Tỉ lệ val mặc định 0.2.
Sequence được lấy từ tên file ảnh trong lô (submission/<batch_id>/images).
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SUBMISSION, batch_dir, die, list_files, load_config, parse_img_name, read_csv, write_csv  # noqa: E402


def leaks(rows):
    by = {}
    for r in rows:
        by.setdefault(r["sequence"], set()).add(r["split"])
    return {s: v for s, v in by.items() if len(v) > 1}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--by", choices=["frame", "sequence"])
    ap.add_argument("--val-ratio", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--check")
    ap.add_argument("--out", default=str(SUBMISSION / "analysis" / "split.csv"))
    a = ap.parse_args()

    if a.check:
        rows = read_csv(Path(a.check))
        lk = leaks(rows)
        print(f"{len(rows)} ảnh; sequence nằm ở cả train và val: {len(lk)} {sorted(lk) or ''}")
        sys.exit(1 if lk else 0)
    if not a.by:
        ap.error("cần --by frame|sequence hoặc --check")

    bd = batch_dir(load_config())
    names = [p.name for p in list_files(bd / "images") if p.suffix.lower() == ".jpg"]
    if not names:
        die(f"Không có ảnh trong {bd / 'images'}.")
    seq = {}
    for n in names:
        m = parse_img_name(n)
        if not m:
            die(f"Tên sai quy ước: {n}. Sửa tên trước khi chia tập.")
        seq[n] = m["sequence"]
    rnd = random.Random(a.seed)
    split = {}
    if a.by == "frame":
        order = names[:]
        rnd.shuffle(order)
        k = max(1, round(len(order) * a.val_ratio))
        for i, n in enumerate(order):
            split[n] = "val" if i < k else "train"
    else:
        seqs = sorted(set(seq.values()))
        rnd.shuffle(seqs)
        target = len(names) * a.val_ratio
        val, tot = set(), 0
        for s in seqs:
            if tot >= target:
                break
            val.add(s)
            tot += sum(1 for n in names if seq[n] == s)
        for n in names:
            split[n] = "val" if seq[n] in val else "train"
    rows = [{"image": n, "sequence": seq[n], "split": split[n]} for n in names]
    nv0 = sum(1 for r in rows if r["split"] == "val")
    if abs(nv0 / len(rows) - a.val_ratio) > 0.1:
        print(f"CẢNH BÁO: val chiếm {nv0}/{len(rows)} ảnh, lệch xa {a.val_ratio:.0%}. Một sequence quá dài làm chia mất cân đối: "
              "thử --seed khác hoặc ghi nhận hạn chế này trong impact_analysis.md.")
    write_csv(Path(a.out), ["image", "sequence", "split"], [[r["image"], r["sequence"], r["split"]] for r in rows])
    lk = leaks(rows)
    nv = sum(1 for r in rows if r["split"] == "val")
    print(f"Chia theo {a.by}: train {len(rows) - nv}, val {nv}. Sequence rò rỉ (nằm ở cả hai tập): {len(lk)} {sorted(lk) or ''}")
    print(f"Đã ghi {a.out}")


if __name__ == "__main__":
    main()
