# Phân tích tác động báo lỗi của team AI

## 1. Báo lỗi (chép lại nguyên văn hoặc tóm tắt)
<<>>

## 2. Ảnh cần mở lại

### Tầng (a): đúng như team AI báo
- Bộ lọc dùng (guideline, sequence, lớp): <<>> — lệnh `trace_query.py` đã chạy: <<>>
- Danh sách ảnh (tên đầy đủ): <<>>

### Tầng (b): rủi ro hệ thống (cùng nguyên nhân, chưa ai báo)
- Vì sao có tầng này: <<>>
- Danh sách ảnh (tên đầy đủ): <<>>

## 3. Báo ai
| Người | Vai | Báo gì |
|---|---|---|
| <<>> | <<gán / kiểm>> | <<>> |

## 4. Lô sửa
- Tên lô: <<lo_NNN_v2>> — **không ghi đè lo_NNN_v1**, vì: <<>>
- Thay đổi: <<ảnh/nhãn nào đổi>>; giữ nguyên: <<>>
- Cập nhật: README.txt (Ghi chú, Guideline), manifest, label_summary, qc_report (QC lại ảnh nào), truyvet, hash mới: <<>>

## 5. Có truy vết vs không có truy vết
<<Cùng báo lỗi này: có truyvet.csv phải mở lại bao nhiêu ảnh (trên tổng bao nhiêu); không có truyvet thì sao? Tính bằng số của lô bạn.>>

## 6. Chia tập
- Chia theo frame (cách sai): <<chép dòng kết quả `make_split.py --by frame`>>
- Chia theo sequence (cách đúng): <<chép dòng kết quả>>
- Giải thích: vì sao chia theo frame làm điểm đánh giá cao giả? Vì sao sequence ID phải duy nhất toàn lô? <<>>
