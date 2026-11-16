# Checkpoints — Day 10

Bài **cá nhân**, dự kiến **180 phút (3 giờ)**. Các mốc tính từ lúc bắt đầu, là điểm **tự kiểm tra** tại lớp, **không phải hạn nộp**. Deadline do giảng viên/coach thông báo.

| Mốc | Mục tiêu | Tự kiểm tra |
|---|---|---|
| 0:10 | **CP0** Chuẩn bị | `lab_config.json` đã điền; Python ≥ 3.9 chạy được; đã chọn Track A/B và có đủ giấy tờ nguồn. |
| 1:05 | **CP1** Kiểm file xuất | `kiem_lo.py` chạy được (có `--out`); `mutation_test.md` có 3 lỗi cài; `bug_ticket.md` đã commit; `check_report_export2.txt` kết luận ĐẠT. |
| 2:00 | **CP2** Chuẩn hoá + đóng gói | `rename_map.csv`, `seq_remap.csv` xong; `lo_NNN_v1/` đủ bốn phần **kể cả `truyvet.csv`** (chưa cần hash). |
| 2:30 | **CP3** Chia tập, báo lỗi | `split.csv` không rò rỉ; `impact_analysis.md` có hai tầng ảnh cần mở lại và tên lô mới. |
| 3:00 | **CP4** Nộp | `security.md` đủ 4 mục; `pack_batch.py` ra hash, phiếu đã điền; `check_batch.py` không còn FAIL; `receive_batch.py` không còn câu hỏi; `individual_note.md` xong; đã nộp link. |

## Cần hiểu ở từng mốc

### CP1
Vì sao script **im lặng** chưa chứng minh file sạch? (mutation test) · Tên lớp `person` và `"person "` máy đếm là mấy lớp? · Chênh dù **một nhãn** giữa CVAT và file xuất: vì sao phải giải thích trước khi nộp?

### CP2
Vì sao đổi tên ảnh mà không sửa `file_name` trong file nhãn làm hỏng cả lô? · Hai đoạn thu cùng mã `seq001`: team AI chia train/val sẽ gặp gì? · Bốn phần của lô là gì, thiếu một thì sao? · Ba câu hỏi truy vết mỗi ảnh: ai gán, ai kiểm, guideline nào; nguồn nào CVAT **không** tự ghi?

### CP3
Chia theo frame vs theo sequence: rò rỉ dữ liệu là gì? · Khoanh vùng nhỏ nhất: bao nhiêu ảnh thay vì cả lô? · Vì sao có hai tầng ảnh cần mở lại?

### CP4
Hash chứng minh điều gì, **không** chứng minh điều gì? · Vì sao lô mới phải có tên mới thay vì ghi đè? · Thấy khuôn mặt rõ trong lô: vì sao **Hold + báo người phụ trách** chứ không tự xử lý? · PASS của script có nghĩa nhãn đúng không?

Chi tiết lệnh xem [GUIDE.md](GUIDE.md). Nếu CVAT chậm hoặc không vào được: Track B vẫn làm đủ không cần CVAT. Nếu quá giờ ở Pha 1/2, báo coach: cho phép làm tiếp ngoài giờ theo hạn nộp.
