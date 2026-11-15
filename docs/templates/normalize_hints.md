# Gợi ý chuẩn hoá metadata (đọc nhưng tự viết)

Không có lời giải ở đây, chỉ các mẹo để khỏi mất thời gian vào chỗ không phải trọng tâm.

- **Ngày** có nhiều kiểu cùng lúc (`2026-11-05`, `05/11/2026`, `3/11/26`, `20261105`). Nhận biết kiểu bằng độ dài và ký tự ngăn; kiểu `d/m/y` luôn là ngày trước tháng (xem `capture_log_README.md`). Năm hai chữ số thì thêm `2000`. Kiểm bằng `datetime.date(y, m, d)`: ngày không tồn tại sẽ báo lỗi.
- **Camera** ánh xạ về F hoặc B bằng một từ điển nhỏ, so sánh sau khi `.lower()`: ví dụ `{"camf": "F", "front": "F", ...}`. Gặp giá trị chưa có trong từ điển thì **dừng và thêm**, đừng đoán.
- **Số** (xe, sequence, frame): lấy chữ số bằng `re.sub(r"\D", "", s)`; cẩn thận chuỗi rỗng.
- **Mã xe trống**: tìm các dòng khác cùng (ngày, camera, sequence) rồi lấy mã xe của chúng.
- **Sequence trùng mã**: gom các dòng liên tiếp có cùng (xe, ngày, camera, sequence) thành một "đoạn thu", rồi xét từng đoạn theo quy tắc ở GUIDE Pha 2.2.
- **Kiểm** bằng `python scripts/check_names.py --dir <thư mục>` sau khi đổi tên.
- Làm bằng Excel/Google Sheets cũng được: lưu **CSV UTF-8 (Comma delimited)**, dấu phẩy.
