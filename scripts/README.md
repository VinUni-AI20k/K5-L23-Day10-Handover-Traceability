# Scripts của lab

Chạy **từ thư mục gốc repo**. Python 3.9+, chỉ dùng thư viện chuẩn (không cần `pip install`). Mọi script có `--help` (không chạy gì khi bạn gõ `--help`). Đọc `lab_config.json` để biết tên lô.
**Không sửa** các script này (xem [RULES.md](../RULES.md)). Script **kiểm file xuất (`kiem_lo.py`) do bạn tự viết**, không nằm ở đây.

## Thứ tự dùng

| Pha | Script | Việc | Ghi |
|---|---|---|---|
| 2 | `check_names.py` | kiểm tên file theo quy ước, giải thích từng chỗ sai | (màn hình) |
| 2 | `apply_rename.py` | đổi tên ảnh theo `rename_map.csv` + sửa `file_name` trong nhãn | `submission/<lô>/images`, `annotations` |
| 2 | `build_manifest.py` | liệt kê file + sha256 | `<lô>/manifest.csv` |
| 2 | `build_label_summary.py` | số nhãn theo lớp | `<lô>/label_summary.csv` |
| 4 | `hash_file.py` | sha256 một file; `--verify` so mã | (màn hình) |
| 4 | `pack_batch.py` | zip tái lập + hash | `submission/<lô>.zip`, `<lô>.sha256` |
| 4 | `receive_batch.py` | đóng vai team AI nhận lô | (màn hình) |
| 3 | `make_split.py` | chia train/val theo frame (sai) hoặc sequence (đúng), kiểm rò rỉ | `submission/analysis/split.csv` |
| 3 | `trace_query.py` | lọc `truyvet.csv` theo guideline/người/sequence/lớp | (màn hình) |
| 4 | `check_batch.py` (hoặc `check_submission.py`, cùng việc) | bộ kiểm cuối, mã A–G (xem [RUBRIC.md](../RUBRIC.md)) | (màn hình), `--json` |

## Mã kiểm của `check_batch.py`

| Nhóm | Mã | Kiểm |
|---|---|---|
| A cấu trúc | A1–A7 | thư mục lô, không file lạ, đủ phần, một file nhãn, tên nhãn theo phiên bản, ảnh, ATTRIBUTION có cột `new_name` |
| B file xuất | B1–B12 | JSON mở được, tên lớp, id, ảnh khớp, box trong ảnh, w/h > 0, kích thước ảnh, summary, TOTAL, đối soát CVAT |
| C manifest/hash | C1–C3 | manifest đúng thư mục, sha256 từng file, zip tái lập khớp `.sha256` |
| D metadata/truy vết | D1–D9 | tên ảnh, sequence duy nhất, frame, manifest khớp tên, `truyvet.csv`, split |
| E số liệu | E1–E12 | README đủ mục và khớp thật, QC, kết luận hợp ngưỡng |
| F phiếu, bảo mật | F1–F8 | phiếu, hash, checklist 5 mục, kết luận nhất quán, `security.md` |
| G bằng chứng | G-* | file trong `worklog/`, `kiem_lo.py` tự viết (AST), **bộ kiểm chạy lại `kiem_lo.py`**: G-run1/G-run2 (export_1 KHÔNG ĐẠT, export_2 ĐẠT), G-rep1 (báo cáo = output thật), G-ticket (ticket nêu đủ lỗi), G-mut (script bắt 3 lỗi cài ẩn); `impact_analysis.md`; không còn `<<...>>` |

`PASS` là đúng **định dạng và nhất quán**. Nội dung nhãn đúng hay sai là việc QC của người; chất lượng giải thích của bạn do người chấm đọc.
