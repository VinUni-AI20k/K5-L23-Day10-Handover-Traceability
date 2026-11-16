# Rubric review lab Day 10 (dành cho subagent đóng vai học viên)

Người review **đóng vai học viên** vừa học xong slide Day 10 và nhận repo lab. Mục tiêu: tìm mọi thứ khiến một học viên thật **kẹt, hiểu sai, mất thời gian, hoặc "qua bài" mà không học được gì**.
**Chỉ review, không làm bài thật** (không điền sản phẩm, không viết `kiem_lo.py`, không hoàn thành pha nào). Được đọc mọi file, và chạy script ở chế độ chẩn đoán trên **bản sao riêng** (`--help`, `check_names.py`, `check_batch.py` trên repo trắng, thử một mẫu nhỏ để kiểm một nghi vấn cụ thể).

## Cách chấm

Mỗi tiêu chí chấm **1–5** (5 = xuất sắc, 3 = chấp nhận được nhưng có chỗ gây kẹt, 1 = không dùng được). **Mỗi điểm ≤ 3 phải kèm bằng chứng** (`file:dòng` hoặc lệnh + output). Không đưa nhận xét chung chung.

| Mã | Tiêu chí | Điểm 5 là | Điểm 1 là |
|---|---|---|---|
| R1 | **Bám slide và mục tiêu** | mọi khái niệm slide (4 phần lô, 4 câu kiểm, hash, metadata, sequence/leakage, truy vết, phân quyền/NDA, checklist 5 mục) đều có bài tập tương ứng; không có việc ngoài slide mà không giải thích | bỏ sót khái niệm lớn hoặc đòi kiến thức chưa dạy |
| R2 | **Rõ ràng, tự theo được** | từ README → GUIDE đi hết bài không phải hỏi ai; mỗi bước có đường dẫn, lệnh, sản phẩm, điều kiện xong | phải đoán ở nhiều bước |
| R3 | **Khả thi trong 4 giờ** | ước lượng thời gian từng pha khớp bảng thời gian ±20% với học viên trung bình | một pha vượt gấp đôi |
| R4 | **Dữ liệu và hai track** | Track B tự đủ; Track A có điều kiện rõ, khả thi, không mâu thuẫn; lỗi cài sẵn đáng học; không đáp án lộ ra | thiếu dữ liệu, mâu thuẫn giữa file, Track A không làm nổi |
| R5 | **Script và bộ kiểm** | chạy đúng, thông báo lỗi giúp sửa được, không có bug, không phụ thuộc OS, `--help` rõ | lỗi/bug làm học viên kẹt hoặc kết luận sai |
| R6 | **Giá trị học và chống lách** | bài buộc suy nghĩ; không thể "qua" bằng cách dán một prompt vào AI hoặc điền cho khớp checker; có chỗ đánh giá hiểu thật | có thể qua bằng thao tác máy móc |
| R7 | **Rubric chấm điểm** | mỗi mục đo được, có bằng chứng, nhất quán với GUIDE và bộ kiểm, công bằng cho Track A/B, chặn gian lận | mâu thuẫn, mơ hồ, hoặc điểm không gắn với thứ học viên làm |
| R8 | **Bảo mật, giấy phép, đạo đức dữ liệu** | hướng dẫn không dẫn học viên vào vi phạm (commit dữ liệu riêng tư, dán dữ liệu thật vào AI, thiếu ghi công) và tự thực hành điều bài dạy | bài tự mâu thuẫn với nguyên tắc nó dạy |
| R9 | **Nhất quán tài liệu** | đường dẫn, tên file, lệnh, số liệu, mã kiểm khớp nhau giữa README/GUIDE/RULES/RUBRIC/SUBMISSION/CHECKPOINTS/templates/scripts/cheatsheet | nhiều mâu thuẫn, link/đường dẫn hỏng |

## Quy tắc ghi finding

Mỗi finding gồm: `id` (F01…), `severity` (BLOCKER = không làm tiếp được / MAJOR = hiểu sai hoặc mất > 15 phút hoặc qua bài không học / MINOR / NIT), `tiêu chí` (R1–R9), `vị trí` (`file:dòng`), `tình huống học viên gặp` (cụ thể, "tôi làm bước X thì ..."), `bằng chứng` (trích dòng hoặc lệnh+output), `đề xuất sửa` (cụ thể, có thể áp dụng ngay).
Không trùng lặp finding. Phân biệt rõ **sự thật đã kiểm chứng** với **phỏng đoán**.

## Bắt buộc có trong báo cáo

1. Bảng điểm R1–R9 (1–5) kèm một câu lý do mỗi dòng.
2. Bảng **ước lượng thời gian** từng pha (P0–P6) cho persona của bạn so với thời gian đề ra, kèm lý do chỗ chênh.
3. Danh sách finding, sắp theo severity.
4. **"Những câu tôi sẽ phải hỏi giảng viên"** (≥ 5 câu thực tế nếu có).
5. **Top 5 sửa quan trọng nhất** (xếp theo tác động).
6. Mục "Điều làm tốt" (≤ 5 dòng): giữ lại.
7. Kết luận: có nên phát hành cho lớp ngay không (Có / Có sau khi sửa BLOCKER+MAJOR / Không), một câu lý do.

Báo cáo viết bằng **tiếng Việt**, tối đa khoảng 2.500 từ, ưu tiên dày bằng chứng hơn dài dòng.
