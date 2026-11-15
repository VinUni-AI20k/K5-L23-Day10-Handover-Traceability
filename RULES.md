# Quy tắc làm bài

## Hình thức

**Bài cá nhân.** Mỗi người một lô, một repo (hoặc một nhánh riêng nếu lớp dùng chung repo; theo hướng dẫn coach). Có thể thảo luận khái niệm với bạn cùng lớp,
nhưng **sản phẩm (script, báo lỗi, phiếu, truy vết, phân tích) do bạn tự làm**. Hai bài giống nhau từng dòng sẽ bị hỏi lại.

## Chọn dữ liệu

- **Track B** dùng `data/starter/`. Nhãn là nhãn luyện tập tổng hợp; không dùng nó làm "kết quả gán nhãn" ở bất kỳ nơi nào khác.
- **Track A** dùng lô của bạn. Chỉ dùng ảnh **công khai hoặc giấy phép mở** (ảnh Day 7 là CC BY / CC BY-SA / CC0). Ảnh riêng tư, ảnh có người quen, ảnh từ công ty/dự án có NDA
  **không được commit** vào repo; nếu chọn dữ liệu như vậy, đặt `"images_private": true` trong `lab_config.json`, nộp thư mục lô **không có `images/`** (bộ kiểm bỏ phần kiểm thư mục ảnh) và nói rõ trong `security.md` (hash và manifest vẫn nộp được).
- Starter pack có ảnh người thật và biển số (ảnh công khai CC dùng cho học tập): chỉ dùng cho lab này, không dùng vào việc khác. Trong dự án thật, thấy mặt/biển số rõ thì Hold (xem `security.md`).
- Giữ nguyên `ATTRIBUTION.csv` của ảnh Wikimedia (ghi công theo giấy phép) và đưa nó vào lô.

## Trung thực của số liệu

- **Không tự bịa** số nhãn, số ảnh lỗi, hash, tên người gán/kiểm, kết quả QC. Track B: chỉ dùng số từ `data/starter/`. Track A: số từ CVAT / báo cáo QC thật của bạn.
- Số trong README, phiếu, `label_summary.csv` phải **khớp file thật** (bộ kiểm so từng số). Nhưng khớp chưa đủ: bạn phải **hiểu vì sao**. Người chấm có thể hỏi bất kỳ con số nào.
- Kết luận **Rework** hoặc **Hold** hợp lệ khi số liệu đòi hỏi, **không** bị trừ điểm. **Báo Release trong khi số liệu không đạt thì bị trừ điểm nặng.**
- Không sửa `data/starter/**` (kể cả hai file export). Không xoá file ẩn "để qua bộ kiểm": bộ kiểm đã tự bỏ qua `.DS_Store`/`Thumbs.db`. Mọi thứ bạn tạo nằm trong `submission/`.
- Không sửa `scripts/` để "qua" bộ kiểm. Tìm thấy bug thật thì ghi vào `individual_note.md` (sửa gì, vì sao) và báo coach.
- `data/starter/cvat_export_2_reexport/` (Track B) chỉ mở **sau khi** `bug_ticket.md` đã được commit. Lịch sử commit là bằng chứng.

## Dùng AI

- **Được** dùng AI để viết `kiem_lo.py`, giải thích khái niệm, sửa chính tả. **Bắt buộc** ghi prompt và cách bạn kiểm tra kết quả vào `submission/worklog/prompts.md`.
- **Không dán dữ liệu thật** vào AI: không ảnh, không file nhãn thật, không mã người dùng thật. Chỉ dùng **3 dòng dữ liệu giả** (đây cũng là nội dung bài bảo mật).
- **Không** dùng AI để điền phiếu, README, truy vết, phân tích hộ. Phần đó đòi hỏi bạn đọc dữ liệu của chính mình.
- Bạn phải giải thích được từng dòng `kiem_lo.py` nếu được hỏi.

## Độc lập

- Mutation test (Pha 1.3) dùng file giả do **bạn** tự tạo, không copy của bạn khác.
- Pha 6.3 (đổi lô với bạn cùng lớp) chỉ là **nhận lô** bằng `receive_batch.py`, không xem bài nhau.

## Git và nộp bài

- Repo **public** (hoặc theo hướng dẫn coach; `lab_config.json` và tiêu đề README có MSHV/họ tên, vì vậy chỉ dùng tên bạn đồng ý công khai). Commit mang **tên và email của bạn**; **ít nhất một commit mỗi pha** (7 commit trở lên).
  Thứ tự commit phải hợp lý: `bug_ticket.md` trước khi dùng export lần 2; `kiem_lo.py` trước `check_report_export1.txt`.
- Không commit `*.zip`, thư mục `work/`, API key, token, dữ liệu riêng tư.
- Bài chấm theo commit cuối trước hạn. Hạn và kênh nộp do giảng viên/coach công bố; nộp muộn bị trừ điểm.
