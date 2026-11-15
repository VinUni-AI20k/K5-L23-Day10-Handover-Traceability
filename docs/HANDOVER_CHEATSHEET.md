# Tóm tắt kiến thức Day 10 (nhớ nhanh)

Nguồn: slide Day 10 "Bàn giao dữ liệu & Truy vết". Chuỗi dữ liệu: Gán nhãn → Kiểm (QC) → Xuất file → **Đóng gói** → **Team AI**. Lô sai định dạng hoặc thiếu metadata thì dừng ngay ở bước đóng gói.

## 1. Lô bàn giao gồm bốn phần

| Phần | Là | Nằm ở |
|---|---|---|
| Danh sách file | tên từng ảnh và file nhãn, kèm hash | `manifest.csv` |
| Số lượng nhãn | tổng và theo từng lớp | `label_summary.csv` |
| Phiên bản guideline | gán theo luật nào | `README.txt` (+ `truyvet.csv` từng ảnh) |
| Báo cáo QC | mẫu kiểm, tỉ lệ đạt, kết luận | `qc_report.txt` |

Thiếu một phần thì lô **chưa được coi là bàn giao**. Một lô một thư mục một số phiên bản; không file rời; **mỗi phiên bản một tên mới, không ghi đè lô đã nộp**.

```
lo_017_v1/
├─ images/   ├─ annotations/   ├─ manifest.csv   ├─ label_summary.csv   ├─ qc_report.txt   ├─ README.txt   └─ truyvet.csv
```

## 2. Bốn câu kiểm file xuất (phải trả lời Có)

| Câu | Kiểm bằng | Lỗi hay gặp |
|---|---|---|
| Mở lại được | giải nén, đọc JSON, nhập lại CVAT (task mới, *Replace*) | file hỏng, thiếu khoá |
| Đúng tên lớp | so **từng ký tự** với taxonomy | `Car`, `"person "`, `xe_hoi`, `pedestrian` |
| Đủ số nhãn | Info từng job (CVAT) = file xuất, theo lớp | ảnh thiếu, nhãn mất |
| Đúng định dạng | box trong ảnh, w/h > 0, đúng format yêu cầu | box ngoài ảnh, đổi tên ảnh mà không sửa nhãn |

PASS của script = **đúng định dạng**, không phải nhãn đúng. QC của người vẫn bắt buộc.

COCO `bbox = [x, y, rộng, cao]`, gốc tọa độ ở góc trên trái. Góc dưới phải = `(x + rộng, y + cao)`.

## 3. Hash (sha256)

Đổi một bit thì mã đổi hoàn toàn. Dùng để chứng minh **file không bị đổi trên đường đi** (team AI chạy lại và so hai mã). Hash **không** chứng minh nhãn đúng, chỉ chứng minh "đây đúng là file bạn gửi".
Lệnh: `python scripts/hash_file.py <file>` (hoặc `shasum -a 256` / `sha256sum` / `certutil -hashfile <file> SHA256`).

## 4. Metadata và tên file

Mẫu: `vehNN_YYYYMMDD_camX_seqNNN_NNNNNN.jpg` — xe · ngày · camera (F/B/L/R) · sequence · frame.

| Lỗi | Hậu quả |
|---|---|
| ngày `3/11/26` | mơ hồ ngày hay tháng |
| `front`, `trước`, `CamF` lẫn nhau | đếm camera sai |
| sequence đặt lại từ 1 | hai đoạn **trùng mã**, chia tập sai |
| thiếu mã xe | không truy ra nguồn |

Quy tắc lab: sequence ID **duy nhất toàn lô**; ngày trong CSV `2026-11-05`, trong tên file `20261105`.

**Rò rỉ dữ liệu (data leakage):** frame liền nhau gần như giống hệt; nếu cùng sequence nằm ở cả train và val thì điểm đánh giá cao giả. Chia theo **sequence**, không theo frame.

## 5. Truy vết

Mỗi ảnh trả lời: **ai gán · ai kiểm · guideline nào**. Ghi ngay khi làm.

| Cột | Lấy từ | Ai ghi |
|---|---|---|
| Người gán | CVAT: người được giao job (assignee) | tự có, chép ra |
| Người kiểm | phiếu QC của job | người QC ghi |
| Guideline | phiên bản ghi ở đầu job | quản trị ghi |

CVAT **không** tự ghi người kiểm và guideline. Có truy vết: lỗi xe bán tải chỉ cần mở lại ~312/5.000 ảnh; không có: kiểm lại cả dự án. Khoanh vùng nhỏ nhất có thể.

## 6. QC và ngưỡng (nối Day 7)

- Lô < 500 ảnh: kiểm 100%; lô lớn: mẫu ≥ 10% và tối thiểu 50 ảnh.
- Ngưỡng Release: **≤ 2% ảnh có lỗi** (≥ 98% đạt). Luôn ghi **mẫu số**: `49/50 = 98%`.
- Cây quyết định: **Hold** (guideline chưa rõ / dữ liệu hỏng) → **Rework** (> 2% lỗi, lỗi lặp, IoU/IAA dưới ngưỡng) → **Release**.
- Có hai vòng (trước và sau sửa): ghi **cả hai** và nói rõ số nào dùng để kết luận.

## 7. Bảo mật

| Nguyên tắc | Nghĩa | Ví dụ vi phạm |
|---|---|---|
| Phân quyền | chỉ mở job được giao; quyền tối thiểu | đưa tài khoản CVAT cho đồng nghiệp |
| Dữ liệu ở lại | không tải ra ngoài hệ thống được cấp | USB, email cá nhân, dán nhãn thật lên chatbot |
| NDA | ảnh, nhãn, quy trình là thông tin mật, cả sau dự án | chụp màn hình cảnh xe gửi người quen |

Thấy khuôn mặt rõ mà guideline yêu cầu làm mờ: **Hold lô, báo người phụ trách**; không tự xử lý, không xoá ảnh, không hỏi nhóm chat chung.
Với trợ lý AI: chỉ gửi **dữ liệu giả**.

## 8. Checklist bàn giao cuối cùng

Đủ bốn phần · file xuất qua bốn câu kiểm · metadata đủ bốn trường · truy vết (gán, kiểm, guideline) · dữ liệu ở lại hệ thống. Đủ năm mục mới nộp.
