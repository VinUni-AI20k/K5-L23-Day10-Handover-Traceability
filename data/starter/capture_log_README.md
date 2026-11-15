# Nhật ký thu (capture_log.csv)

Người thu ghi tay, mỗi người một thói quen; **chưa chuẩn hoá**. Việc của bạn là chuẩn hoá theo quy ước lô bàn giao (xem `docs/HANDOVER_CHEATSHEET.md`).

- Ngày ghi theo **ngày/tháng/năm** (dd/mm/yy hoặc dd/mm/yyyy) hoặc ISO `YYYY-MM-DD` hoặc `YYYYMMDD`. Không có dạng tháng/ngày.
- `camera`: trước = F, sau = B (mọi cách ghi khác như front/rear/trước/sau đều quy về hai chữ này).
- `frame`: số thứ tự khung trong đoạn thu.
- Mỗi `sequence` là **một đoạn thu liên tục của một camera trên một xe trong một ngày**.
- Mã `sequence` ở nhật ký là mã người thu tự đặt trên từng xe; **hai xe/hai ngày có thể trùng mã**.
- Dòng trống ở cột `vehicle`: người thu quên ghi; xe đó trùng với các ảnh cùng đoạn (cùng sequence, cùng ngày).

> Metadata này là **dữ liệu luyện tập** gán cho 40 ảnh Day 7, không phải thông tin thật của ảnh Wikimedia.
