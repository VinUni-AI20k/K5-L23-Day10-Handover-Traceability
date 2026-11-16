# Tóm tắt review lab bằng học viên giả lập

Ba subagent đóng vai học viên đọc và chẩn đoán lab theo [../RUBRIC_REVIEW.md](../RUBRIC_REVIEW.md) (chỉ review, không làm bài thật):

| Persona | Góc nhìn | Kết luận vòng 1 |
|---|---|---|
| Lan (L2, Windows, Python yếu, Track B) | tự theo được, thời gian, lệnh trên Windows | Phát hành sau khi sửa lệnh Windows, thứ tự pha, thời gian |
| Minh (L3, macOS, Track A) | Track A làm nổi không, bug script, công bằng rubric | Phát hành sau khi sửa đường Track A, file ẩn, zip tái lập |
| Quân (tìm đường tắt) | chống lách, rubric ↔ bộ kiểm, dữ liệu nhất quán | Phát hành sau khi bộ kiểm chạy lại `kiem_lo.py` và đối chiếu số liệu |

## Đã sửa sau vòng 1
- Lệnh tách theo Windows/macOS, script tự in UTF-8, `kiem_lo.py` có `--out`.
- `truyvet.csv` chuyển lên Pha 3 (đóng gói và ghi hash một lần); thời gian đặt lại 4,5 giờ.
- Bộ kiểm: bỏ file ẩn, zip tái lập mọi hệ điều hành, chạy lại `kiem_lo.py` (export_1 KHÔNG ĐẠT / export_2 ĐẠT / lỗi cài ẩn), báo cáo phải là output thật, `bug_ticket.md` nêu đủ lỗi, `security.md` kiểm theo mục.
- Track A: quy ước riêng, mã giả danh, `images_private`, `allow_same_reviewer`, bảng điểm thay thế.
- Rubric: bậc điểm, vấn đáp 5 phút, đáp án QC hai vòng, định nghĩa tầng (a)/(b).

## Còn lại (ghi nhận)
- Đáp án Track B giống nhau giữa học viên (giảm rủi ro bằng vấn đáp, chưa sinh biến thể theo MSHV).
- `cvat_export_2_reexport/` nằm trong repo; chỉ ràng buộc bằng quy tắc và kiểm nội dung `bug_ticket.md`.
