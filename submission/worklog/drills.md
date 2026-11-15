# Bài luyện nhanh (làm trước khi chạy `check_names.py` để tự kiểm)

## 1. Tìm lỗi trong 6 tên file và viết lại đúng
Mẫu: `vehNN_YYYYMMDD_camX_seqNNN_NNNNNN.jpg`

| # | Tên đã cho | Sai ở đâu | Viết lại đúng |
|---|---|---|---|
| 1 | veh03_20261105_camF_seq017_000001.jpg | <<>> | <<>> |
| 2 | veh03_20261105_camF_seq017_000002.jpg | <<>> | <<>> |
| 3 | veh03_051125_camF_seq017_000003.jpg | <<>> | <<>> |
| 4 | veh03_20261105_front_seq018_000001.jpg | <<>> | <<>> |
| 5 | 20261105_camB_seq018_000002.jpg | <<>> | <<>> |
| 6 | veh03_20261105_camB_seq1_000003.jpg | <<>> | <<>> |

## 2. Ghi metadata thành tên file
- Ảnh 1: xe 07, ngày 3/11/2026, camera sau (B), đoạn 5, frame 42 → <<>>
- Ảnh 2: xe 03, ngày 5/11/2026, camera trước (F), đoạn 9, frame 7 → <<>>

## 3. Đổi một ký tự, mã hash đổi
- `thu.txt` nội dung 1: `<<>>` → sha256: `<<>>`
- sau khi đổi một ký tự: `<<>>` → sha256: `<<>>`
- Nhận xét (bao nhiêu ký tự giống nhau giữa hai mã?): <<>>

## 4. Khoanh vùng: team AI nhắn "Xe bán tải trong seq017 vẫn gán car" (guideline v1.3 đổi bán tải từ car sang truck)

| Ảnh | Người gán | Guideline |
|---|---|---|
| img_000201 | A03 | v1.2 |
| img_000202 | A03 | v1.3 |
| img_000203 | A09 | v1.2 |
| img_000204 | A09 | v1.3 |

- Giả sử cả bốn ảnh thuộc seq017. Ảnh nào cần mở lại: <<>> — báo ai: <<>> — lô mới đặt tên: <<>>

## 5. Chấm một lô bàn giao mẫu

Lô mẫu: `final_moi.zip` chứa `anh xe (1).jpg`, `nhan_sua.json`, `nhan_sua (2).json`; nhãn tên `Car` và `person`; không có số nhãn, không có báo cáo QC; ngày ghi `3/11`, không ghi camera và guideline; không có README.

Tìm **ít nhất 4 điểm chưa đạt** và cách sửa (so với lô tốt trong cheatsheet):

| # | Điểm chưa đạt | Cách sửa |
|---|---|---|
| 1 | <<>> | <<>> |
| 2 | <<>> | <<>> |
| 3 | <<>> | <<>> |
| 4 | <<>> | <<>> |
