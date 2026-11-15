# Checkpoints — Day 10

Bài **cá nhân**, dự kiến **270 phút (4,5 giờ)**. Các mốc tính từ lúc bắt đầu, là điểm **tự kiểm tra** tại lớp, **không phải hạn nộp**. Deadline do giảng viên/coach thông báo.

| Mốc | Mục tiêu | Tự kiểm tra |
|---|---|---|
| 0:15 | **CP0** Chuẩn bị | `lab_config.json` đã điền; Python ≥ 3.9 chạy được; đã chọn Track A/B và có đủ giấy tờ nguồn. |
| 1:25 | **CP1** Kiểm file xuất | `kiem_lo.py` chạy được (có `--out`); `mutation_test.md` có bảng ≥ 5 lỗi cài; `bug_ticket.md` đã commit; `check_report_export2.txt` kết luận ĐẠT. |
| 2:15 | **CP2** Metadata | `rename_map.csv` đủ ảnh; `seq_remap.csv` đã quyết; `lo_NNN_v1/images`, `annotations`, `ATTRIBUTION.csv` đã có và file nhãn khớp tên mới. |
| 3:20 | **CP3** Đóng gói + truy vết | Đủ bốn phần **kể cả `truyvet.csv`**; `pack_batch.py` ra hash; `phieu_ban_giao.md` đã điền; `receive_batch.py` không còn câu hỏi. |
| 3:55 | **CP4** Chia tập, báo lỗi | `split.csv` không rò rỉ; `impact_analysis.md` có hai tầng ảnh cần mở lại và tên lô mới. |
| 4:10 | **CP5** Bảo mật | `security.md` đủ 7 mục. |
| 4:30 | **CP6** Nộp | `check_batch.py` không còn FAIL; `individual_note.md` xong; đã commit mỗi pha; đã nộp link. |

## Cần hiểu ở từng mốc

### CP1
Vì sao script **im lặng** chưa chứng minh file sạch? (mutation test) · Tên lớp `person` và `"person "` máy đếm là mấy lớp? · Chênh dù **một nhãn** giữa CVAT và file xuất: vì sao phải giải thích trước khi nộp?

### CP2
Vì sao đổi tên ảnh mà không sửa `file_name` trong file nhãn làm hỏng cả lô? · Hai đoạn thu cùng mã `seq001`: team AI chia train/val sẽ gặp gì?

### CP3
Bốn phần của lô là gì, thiếu một thì sao? · Hash chứng minh điều gì, **không** chứng minh điều gì? · Vì sao lô mới phải có tên mới thay vì ghi đè? · Ba câu hỏi truy vết mỗi ảnh: ai gán, ai kiểm, guideline nào; nguồn nào CVAT **không** tự ghi?

### CP4
Chia theo frame vs theo sequence: rò rỉ dữ liệu là gì? · Khoanh vùng nhỏ nhất: bao nhiêu ảnh thay vì cả lô? · Vì sao có hai tầng ảnh cần mở lại?

### CP5
Ba nguyên tắc (phân quyền, dữ liệu ở lại, NDA) mỗi cái chặn đường rò nào? · Thấy khuôn mặt rõ trong lô: vì sao **Hold + báo người phụ trách** chứ không tự xử lý?

### CP6
PASS của script có nghĩa nhãn đúng không? · Checklist 5 mục: mục nào script kiểm được, mục nào chỉ người kiểm được?

Chi tiết lệnh xem [GUIDE.md](GUIDE.md). Nếu CVAT chậm hoặc không vào được: Track B vẫn làm đủ P1–P6 không cần CVAT. Nếu quá giờ ở P1/P2, báo coach: cho phép làm tiếp ngoài giờ theo hạn nộp.
