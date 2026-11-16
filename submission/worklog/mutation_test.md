# Mutation test cho kiem_lo.py

> Chứng minh script **bắt được lỗi**: tạo file giả nhỏ (3 ảnh / 5 box, tự làm tay), cài từng lỗi, chạy script.

- File sạch dùng làm gốc: `submission/worklog/fixture_clean.json` (mẫu: `docs/templates/fixture_clean.json`); bản hỏng ở `submission/worklog/mutants/` (<<mô tả: bao nhiêu ảnh, box, lớp>>)
- Script có kết luận ĐẠT trên file sạch: <<có / không + dòng bằng chứng>>

| # | Lỗi cài | Cách cài (một dòng) | Script có bắt? | Bằng chứng (dòng output) |
|---|---|---|---|---|
| 1 | tên lớp sai (`Car` hoặc dấu cách thừa) | <<>> | <<>> | <<>> |
| 2 | thiếu một ảnh | <<>> | <<>> | <<>> |
| 3 | box ngoài ảnh | <<>> | <<>> | <<>> |

## Script bỏ sót lỗi nào, đã sửa gì
<<Nếu cả 3 lỗi đều bắt ngay lần đầu thì thử thêm một lỗi khác bạn nghĩ ra (box rộng 0, nhãn ít hơn CVAT) và ghi vào bảng.>>
