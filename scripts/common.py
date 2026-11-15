"""Hàm dùng chung cho các script của lab Day 10 (chỉ dùng thư viện chuẩn Python 3.9+).

Học viên KHÔNG cần sửa file này. Script `kiem_lo.py` của bạn phải tự viết, không import từ đây.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "lab_config.json"
SUBMISSION = ROOT / "submission"
STARTER = ROOT / "data" / "starter"

# lo_017_v1 : ba chữ số, số phiên bản
BATCH_RE = re.compile(r"^lo_(\d{3})_v(\d+)$")
# veh03_20261105_camF_seq017_000123.jpg
IMG_RE = re.compile(r"^veh(\d{2})_(\d{4})(\d{2})(\d{2})_cam([FBLR])_seq(\d{3})_(\d{6})\.jpg$")
GUIDE_RE = re.compile(r"^v\d+\.\d+$")
ANNOT_RE = re.compile(r"^[A-Z]\d{2}$")  # A07, Q03


for _s in (sys.stdout, sys.stderr):  # in tiếng Việt an toàn khi chuyển hướng ra file trên Windows
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

HIDDEN = {"thumbs.db", "desktop.ini", ".ds_store"}


def list_files(d: Path) -> List[Path]:
    """File thật trong thư mục, bỏ file ẩn / file hệ thống (.DS_Store, Thumbs.db, ._*)."""
    if not d.is_dir():
        return []
    return sorted((p for p in d.iterdir() if p.is_file() and not p.name.startswith(".") and p.name.lower() not in HIDDEN),
                  key=lambda p: p.name)


def die(msg: str, code: int = 2) -> None:
    print(f"\nLỖI: {msg}", file=sys.stderr)
    sys.exit(code)


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        die(f"Không thấy {CONFIG_PATH.name}. Hãy điền lab_config.json ở thư mục gốc repo (xem GUIDE.md, Pha 0).")
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    if cfg.get("track") not in ("A", "B"):
        die('lab_config.json: "track" phải là "A" hoặc "B" (chữ hoa).')
    if not cfg.get("mshv") or cfg.get("batch_id") == "lo_000_v1":
        die("lab_config.json chưa điền: cần mshv, ho_ten, batch_id (lo_NNN_v1), submitter_code (Pha 0).")
    if not BATCH_RE.match(cfg.get("batch_id", "")):
        die("lab_config.json: batch_id phải có dạng lo_NNN_v1 (NNN = 3 chữ số, ví dụ lo_234_v1).")
    if not cfg.get("classes"):
        die("lab_config.json: thiếu danh sách classes.")
    return cfg


def batch_dir(cfg: Optional[dict] = None) -> Path:
    cfg = cfg or load_config()
    return SUBMISSION / cfg["batch_id"]


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def read_csv(path: Path) -> List[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, header: List[str], rows: List[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def jpeg_size(path: Path) -> Optional[Tuple[int, int]]:
    """Đọc (rộng, cao) từ header JPEG, không cần Pillow. Trả None nếu không đọc được."""
    try:
        with open(path, "rb") as f:
            if f.read(2) != b"\xff\xd8":
                return None
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                while b == b"\xff":
                    b = f.read(1)
                if not b:
                    return None
                m = b[0]
                if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                    continue
                if m == 0xD9:
                    return None
                ln = struct.unpack(">H", f.read(2))[0]
                if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                    data = f.read(5)
                    h, w = struct.unpack(">HH", data[1:5])
                    return w, h
                f.seek(ln - 2, 1)
    except (OSError, struct.error):
        return None


def parse_img_name(name: str) -> Optional[dict]:
    m = IMG_RE.match(name)
    if not m:
        return None
    veh, y, mo, d, cam, seq, frame = m.groups()
    import datetime
    try:
        datetime.date(int(y), int(mo), int(d))
    except ValueError:
        return None
    return dict(vehicle=f"veh{veh}", date=f"{y}-{mo}-{d}", camera=cam, sequence=f"seq{seq}", frame=frame)


def load_coco(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def coco_class_counts(d: dict) -> Dict[str, int]:
    """Đếm nhãn theo TÊN lớp đúng như ghi trong file (không chuẩn hoá)."""
    name = {c["id"]: c["name"] for c in d["categories"]}
    out: Dict[str, int] = {}
    for a in d["annotations"]:
        n = name.get(a["category_id"], f"<id {a['category_id']} không có trong categories>")
        out[n] = out.get(n, 0) + 1
    return out


def find_annotation_file(bdir: Path) -> Optional[Path]:
    files = sorted((bdir / "annotations").glob("*.json")) if (bdir / "annotations").is_dir() else []
    return files[0] if files else None


def parse_readme_txt(path: Path) -> Dict[str, str]:
    """README.txt dạng 'Khoá:   giá trị' (một cặp trên một dòng; hai cặp trên cùng dòng cách nhau 4+ dấu cách)."""
    out: Dict[str, str] = {}
    text = path.read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        for part in re.split(r"(?<=[^:\s])\s{2,}(?=[^:\d]{1,20}:\s)", line.strip()):
            if ":" in part:
                k, v = part.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def vn_int(s: str) -> Optional[int]:
    """'4.350' -> 4350, '4,350' -> 4350, '500' -> 500."""
    m = re.match(r"\s*(\d[\d.,]*)", s)
    if not m:
        return None
    t = re.sub(r"[.,]", "", m.group(1))
    return int(t) if t.isdigit() else None
