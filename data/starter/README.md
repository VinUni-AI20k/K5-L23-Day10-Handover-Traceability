# Starter pack (Track B)

Dành cho học viên **không có** lô nhãn riêng từ Day 7/9. Gồm 40 ảnh Day 7 + toàn bộ giấy tờ đi kèm một lô giả định `lo_900`.

| Thư mục / file | Là gì | Dùng ở pha |
|---|---|---|
| `images/` | 40 ảnh gốc, tên `img_NNN.jpg` (tên xấu, chưa có metadata) | P2 |
| `capture_log.csv` + `capture_log_README.md` | nhật ký thu, ghi tay, lộn xộn | P2 |
| `cvat_export_1/` | file nhãn COCO người quản trị **xuất lần 1** (chưa kiểm) | P1 |
| `cvat_export_2_reexport/` | file xuất lại sau khi quản trị sửa theo báo lỗi của bạn. **Chỉ mở sau khi nộp xong báo cáo lỗi P1** | P1 (cuối) |
| `cvat_info/jobs.csv`, `job_headers.txt` | số liệu bạn chép từ CVAT (Info từng job, mô tả job) | P1, P4 |
| `qc_forms/` | phiếu QC của từng job (người kiểm Q03/Q05) | P3, P4 |
| `guideline/changelog.md` | lịch sử guideline v1.2 → v1.3 | P4 |
| `incoming/team_ai_ticket.md` | tin nhắn báo lỗi của team AI | P4 |

**Nhãn là nhãn luyện tập tổng hợp** (box đặt ngẫu nhiên có seed), không phản ánh nội dung ảnh; mục tiêu là luyện đóng gói và truy vết, không phải luyện gán nhãn. Metadata (xe, ngày, camera, sequence), người gán và người kiểm cũng là dữ liệu giả định.

Nguồn và giấy phép ảnh: `ATTRIBUTION.csv` (giữ nguyên, kèm theo lô khi bàn giao).
