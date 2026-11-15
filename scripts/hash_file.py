"""SHA-256 chạy được trên Windows / macOS / Linux (thay cho shasum, sha256sum, certutil).

    python scripts/hash_file.py thu.txt                      # in mã băm
    python scripts/hash_file.py lo_234_v1.zip --verify lo_234_v1.sha256   # so với file .sha256 ("<mã>  <tên file>")
    python scripts/hash_file.py lo_234_v1.zip --verify 3a7f...64 ký tự... # so với mã dán vào
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import sha256_file  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--verify", help="mã băm 64 ký tự, hoặc đường dẫn file .sha256")
    a = ap.parse_args()
    p = Path(a.file)
    if not p.is_file():
        print(f"Không thấy file: {p}", file=sys.stderr)
        sys.exit(2)
    h = sha256_file(p)
    print(f"{h}  {p.name}")
    if a.verify:
        v = a.verify.strip()
        if Path(v).is_file():
            v = Path(v).read_text(encoding="utf-8").split()[0]
        ok = v.lower() == h
        print("KHỚP: file không đổi" if ok else "KHÁC: file đã bị đổi hoặc hỏng trên đường đi")
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
