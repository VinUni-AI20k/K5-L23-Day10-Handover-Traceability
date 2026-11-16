"""Trước khi nộp: chạy bộ kiểm cuối (cùng tên với các lab trước). Tương đương `python scripts/check_batch.py`.

    python scripts/check_submission.py [--json out.json]
"""
import runpy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
runpy.run_path(str(Path(__file__).resolve().parent / "check_batch.py"), run_name="__main__")
