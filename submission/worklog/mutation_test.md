# Mutation test cho kiem_lo.py

> Chứng minh script **bắt được lỗi**: tạo file giả nhỏ (3 ảnh / 5 box, tự làm tay), cài từng lỗi, chạy script.

- File sạch dùng làm gốc: `submission/worklog/fixture_clean.json` (mẫu: `docs/templates/fixture_clean.json`); bản hỏng ở `submission/worklog/mutants/` (<<mô tả: bao nhiêu ảnh, box, lớp>>)
- Script có kết luận ĐẠT trên file sạch: <<có / không + dòng bằng chứng>>

| # | Lỗi cài | Cách cài (một dòng) | Script có bắt? | Bằng chứng (dòng output) |
|---|---|---|---|---|
| 1 | tên lớp viết hoa `Car` | <<>> | <<>> | <<>> |
| 2 | tên lớp có dấu cách thừa | <<>> | <<>> | <<>> |
| 3 | thiếu một ảnh | <<>> | <<>> | <<>> |
| 4 | box ngoài ảnh | <<>> | <<>> | <<>> |
| 5 | box rộng 0 | <<>> | <<>> | <<>> |
| 6 | nhãn ít hơn CVAT | <<>> | <<>> | <<>> |

## Script bỏ sót lỗi nào, đã sửa gì
<<Nếu mọi lỗi đều bắt ngay lần đầu thì viết thêm 1–2 lỗi cài khác mà bạn nghĩ ra và thử.>>
