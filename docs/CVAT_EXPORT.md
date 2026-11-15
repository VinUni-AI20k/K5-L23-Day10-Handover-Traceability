# CVAT: xuất, nhập, lấy số nhãn

Dùng **cvat.ai** (cloud, tài khoản miễn phí) hoặc CVAT của lớp. Menu có thể khác đôi chút giữa các phiên bản; ảnh minh hoạ trong slide dùng CVAT 2.8.
**Track B không cần CVAT.** Phần "nhập lại" ở dưới là tuỳ chọn.

## 1. Xuất nhãn (Track A)

1. Mở task, bấm **Ctrl+S** để lưu.
2. **Menu → Export job dataset** (hoặc *Actions → Export task dataset*).
3. **Format**: mặc định *CVAT for images 1.1*; lab dùng **COCO 1.0**. **Save images**: tắt (trừ khi team AI yêu cầu).
4. Đặt tên theo lô, phiên bản, ngày. Tải `.zip` từ trang **Requests**, giải nén; file nhãn nằm ở `annotations/instances_default.json`.
5. Chép vào `submission/worklog/export_1/annotations/instances_default.json` (lần 1), `export_2/` (sau khi sửa).

Cùng một box, ba cách ghi (ảnh 1600×1200):

| Format | Ví dụ | Ghi chú |
|---|---|---|
| CVAT for images 1.1 | `xtl="797" ytl="870" xbr="965" ybr="928"` | hai góc |
| COCO 1.0 | `"bbox": [797, 870, 168, 58]` | x, y, rộng, cao |
| YOLO 1.1 | `0 0.551 0.749 0.105 0.048` | tâm và kích thước, chuẩn hoá 0–1; id lớp theo thứ tự nhãn trong project |

## 2. Lấy số nhãn theo lớp trong CVAT (đối soát)

1. Mở trang **Tasks** → mở task.
2. Mở **từng job** trong task.
3. Bấm **Info** (menu job): xem **số object theo lớp**.
4. **Cộng các job** → số nhãn theo từng lớp của cả lô → ghi vào `submission/worklog/cvat_counts.csv`.

Số nhãn này là "sự thật" để đối chiếu với file xuất. Người gán nên ghi ngay số của job khi nộp job.

## 3. Nhập lại để kiểm (câu "mở lại được")

1. Tạo **task mới**, cùng ảnh, cùng lớp (nhãn trùng **từng ký tự** với taxonomy).
2. **Menu → Upload annotations**, chọn **đúng format** với file xuất (COCO 1.0).
3. Chọn **Replace** (Append sẽ cộng thêm nhãn, đếm sai).
4. Mở vài ảnh và nhìn thấy nhãn; so lại số nhãn trong Info.

## 4. Người được giao và guideline (cho truy vết)

- **Assignee** của job: xem ở trang Task → danh sách job → cột *Assignee*. Đây là nguồn cho cột `annotator`.
- Phiên bản guideline: ghi ở **Description** của task/job. CVAT **không tự ghi** người kiểm và guideline: quản trị phải điền; bạn bàn giao cần có.
