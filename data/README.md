# Dữ liệu

Hai track, cùng quy trình và bộ kiểm.

## Track B — starter pack (`data/starter/`)

Xem [starter/README.md](starter/README.md). 40 ảnh Day 7 (`images/`, tên `img_NNN.jpg`), giấy phép trong `starter/ATTRIBUTION.csv`.
Mọi giấy tờ đi kèm là **giả định để luyện tập**: nhãn tổng hợp, nhật ký thu, người gán (A07, A12, A03), người kiểm (Q03, Q05), phiên bản guideline (v1.2, v1.3).

## Track A — lô của bạn

Điều kiện:

| Yêu cầu | Chi tiết |
|---|---|
| Số ảnh | **≥ 40** ảnh, đã gán nhãn xong trong CVAT, ít nhất 3 lớp |
| Nguồn | ảnh **công khai hoặc giấy phép mở** (ví dụ ảnh Day 7). Ảnh riêng tư: xem [RULES.md](../RULES.md) |
| File xuất | COCO 1.0 từ CVAT (không phải file bạn tự sửa JSON) |
| Giấy tờ tương đương starter | xem bảng dưới |
| Phiên bản guideline | **≥ 2 phiên bản** trong lô (thiếu thì Pha 3.2 không làm được) (ví dụ Day 7: `v1.0` cho ảnh không bị cờ, `v1.1` cho ảnh đã calibration) |
| Người gán / người kiểm | ≥ 2 người gán (có thể là bạn trong các vai/tài khoản Day 7); người kiểm khác người gán |

| Starter có | Track A bạn cần có |
|---|---|
| `cvat_info/jobs.csv` | số nhãn từng lớp theo job (Info trong CVAT) + người được giao + khoảng ảnh |
| `cvat_info/job_headers.txt` | phiên bản guideline của từng job |
| `qc_forms/` | phiếu/báo cáo QC (Day 7/9): người kiểm, mẫu, lỗi, kết luận |
| `capture_log.csv` | nơi bạn biết xe/ngày/camera/đoạn của từng ảnh (hoặc tự đặt mã nhất quán, ghi vào README.txt) |
| `guideline/changelog.md` | lịch sử guideline v1.0 → v1.1 của nhóm bạn ở Day 7 |
| `incoming/team_ai_ticket.md` | bạn tự viết một báo lỗi từ team AI dựa trên một quy tắc đã đổi |

Nếu thiếu giấy tờ nào, **hỏi coach trước khi làm tiếp** (không tự bịa).

### Quy ước riêng cho Track A

- **Cấu hình:** `lab_config.json` thêm `"images_dir"` (đường dẫn thư mục ảnh gốc); export nằm ở `submission/worklog/export_1/` và `export_2/` (xem GUIDE 1).
- **Không cài lỗi vào dữ liệu thật.** Lô sạch ⇒ `bug_ticket.md` ghi "0 lỗi" kèm bằng chứng; điểm hạng mục 1 được tính thay thế như bảng Track A trong [RUBRIC.md](../RUBRIC.md).
- **Mã người:** dùng mã giả danh dạng `A01`, `Q01` (không dùng tên thật). Bảng ánh xạ tên thật ↔ mã **không commit**.
- **Người kiểm:** cần khác người gán. Nếu thật sự không có (một mình làm), đặt `"allow_same_reviewer": true` và giải thích ở README Ghi chú.
- **Metadata:** nếu ảnh không có xe/camera/ngày chụp, tự đặt mã nhất quán, giải thích ở README Ghi chú; sequence = **một lần chụp liên tục** (cùng tác giả/sự kiện/phiên), không mỗi ảnh một sequence.
- **Định dạng ảnh:** lab chỉ hỗ trợ tên `.jpg` chữ thường; ảnh `.png/.jpeg/.JPG` cần đổi sang `.jpg` (chuyển đổi bằng công cụ bạn dùng; ghi vào README Ghi chú).
- **Ticket tầng (a)/(b):** bạn tự dựng từ một quy tắc đã đổi v1.0 → v1.1; xem GUIDE 4.2.
- **Ảnh riêng tư:** `"images_private": true`, không commit ảnh (RULES).
