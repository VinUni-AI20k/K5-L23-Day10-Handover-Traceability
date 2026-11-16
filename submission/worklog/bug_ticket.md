# Báo lỗi file xuất lần 1 — gửi người quản trị CVAT

> Commit file này **trước** khi mở export lần 2 (Track B).

- Lô: <<lo_NNN_v1>> — file kiểm: <<đường dẫn export_1>> — báo cáo: `check_report_export1.txt`

## 1. Tóm tắt
<<Một đoạn: tổng số ảnh/nhãn trong file xuất so với CVAT, kết luận của script.>>

## 2. Lỗi tìm thấy
| # | Loại | Số lượng | Chi tiết cụ thể (id nhãn / tên ảnh / tên lớp, `repr`) | Hệ quả với team AI |
|---|---|---:|---|---|
| 1 | <<tên lớp sai>> | <<>> | <<>> | <<>> |
| 2 | <<ảnh thiếu>> | <<>> | <<>> | <<>> |
| 3 | <<box ngoài ảnh>> | <<>> | <<>> | <<>> |
| 4 | <<box suy biến w/h ≤ 0>> | <<>> | <<>> | <<>> |

## 3. Đối soát số nhãn với CVAT
| Lớp | CVAT | File xuất | Chênh | Giải thích |
|---|---:|---:|---:|---|
| <<>> | <<>> | <<>> | <<>> | <<>> |

Nhãn mất thuộc ảnh nào, bạn tìm ra bằng cách nào: <<>>

## 4. Việc cần làm trong CVAT
<<Từng việc, ai làm, ví dụ đổi tên nhãn trong project, thêm ảnh vào task, kéo box vào trong ảnh. KHÔNG sửa tay file JSON.>>

## 5. Cách tôi kiểm lại sau khi nhận export lần 2
<<Lệnh nào, điều kiện đạt là gì.>>

## 6. Kết quả sau export lần 2
<<Kết luận của check_report_export2.txt. Nhập lại CVAT (Upload annotations, Replace) là tuỳ chọn: nếu làm thì ghi 2–3 dòng kết quả.>>
