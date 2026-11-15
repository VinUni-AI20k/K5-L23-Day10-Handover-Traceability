# Rubric — 100 điểm

Điểm dựa trên **bằng chứng trong repo** và **khả năng giải thích**, không dựa vào việc lô được Release. Lô **Rework/Hold trung thực, có phân tích** vẫn được điểm tốt.
`check_batch.py` cho **bằng chứng định dạng** (PASS/FAIL theo mã kiểm tra bên dưới) và **chạy lại `kiem_lo.py` của bạn**; người chấm đọc phần còn lại. Mỗi mục con chấm theo bậc: **đủ điểm** khi đạt hết tiêu chí, **một nửa** khi đạt phần lớn nhưng có lỗi không nghiêm trọng, **0** khi thiếu hoặc sai căn bản.

**Vấn đáp (bắt buộc, ~5 phút/học viên, người chấm chọn ngẫu nhiên):** (1) giải thích một đoạn tuỳ chọn của `kiem_lo.py` và sửa nó khi đổi yêu cầu; (2) giải thích một con số trong README/phiếu (lấy từ đâu); (3) một ảnh trong tầng (a) hoặc (b): vì sao nó nằm trong tập. Không trả lời được: hạng mục tương ứng tối đa một nửa điểm.

**Track A:** các hạng mục có "đáp án Track B" (bug_ticket 5 điểm, khoanh vùng 7 điểm, sequence trùng 5 điểm) chấm **theo tính nhất quán với bằng chứng của chính bạn + vấn đáp**: lô sạch ghi "0 lỗi" kèm bằng chứng được đủ điểm bug_ticket nếu mutation test chứng minh năng lực bắt lỗi; sequence = nhóm theo lần chụp liên tục có giải thích. Track A có thêm việc (nhập lại CVAT, giấy tờ) nên được **+4 điểm thưởng** (tối đa 100).

| # | Hạng mục | Điểm | Bằng chứng chính |
|---|---|---:|---|
| 1 | Kiểm file xuất, script tự viết, báo lỗi | 20 | `kiem_lo.py`, `mutation_test.md`, `check_report_*`, `bug_ticket.md`, `cvat_counts.csv` |
| 2 | Metadata và đổi tên | 15 | `rename_map.csv`, `seq_remap.csv`, `drills.md`, `check_batch` D1–D4 |
| 3 | Đóng gói lô đủ bốn phần | 20 | thư mục `lo_NNN_v1/`, hash, `phieu_ban_giao.md`, `check_batch` A, C, E |
| 4 | Truy vết và phân tích tác động | 20 | `truyvet.csv`, `split.csv`, `impact_analysis.md` |
| 5 | Bảo mật | 10 | `security.md` (đối chiếu F7, F8) |
| 6 | Trung thực, tái lập, quy trình làm việc | 15 | `check_batch.py`, `receive_batch.py`, lịch sử commit, `prompts.md`, `individual_note.md` |

## 1. Kiểm file xuất (20)
- **6 — Script.** `kiem_lo.py` tự viết, chạy được, đủ 6 yêu cầu (GUIDE 1.2), không sửa file, thoát mã đúng. Mã kiểm: `G-own`, `G-run1`, `G-run2`, `G-mut`. *Mất điểm:* import từ `scripts/`, chỉ in đếm mà không phát hiện lỗi, không `repr` tên lớp (bỏ sót dấu cách thừa), không đối soát CVAT.
- **5 — Mutation test.** Bảng lỗi cài ≥ 5 loại, mỗi loại có bằng chứng script bắt được; lỗi nào script bỏ sót thì đã **sửa script** và ghi lại. *Mất điểm:* chỉ khẳng định "script chạy tốt", file mutation copy từ bạn khác, lỗi cài không chạy lại được.
- **5 — Báo lỗi (`bug_ticket.md`).** Mỗi lỗi có loại, số lượng, **id/tên ảnh cụ thể**, hệ quả với team AI, việc cần làm trong CVAT; **giải thích được chênh lệch số nhãn** (nhãn mất thuộc ảnh nào). Mã kiểm: `G-rep1` (báo cáo là output thật), `G-ticket` (ticket nêu đủ tên lớp sai, id box lỗi, ảnh thiếu như script thấy ở export_1). Người chấm đọc phần hệ quả và việc cần làm trong CVAT. *Mất điểm:* chỉ nói "file có lỗi", không chỉ ra chỗ, không nối lỗi với hệ quả.
- **4 — Trạng thái sau sửa.** `check_report_export2.txt` kết luận ĐẠT; lô nộp dùng export lần 2; (Track A) có ghi kết quả nhập lại CVAT.
- Trừ nặng: `bug_ticket.md` commit **sau** khi dùng export_2 (Track B) hoặc báo cáo kiểm export_1 không phải output thật của script.

## 2. Metadata và đổi tên (15)
- **5 — Chuẩn hoá đúng.** Mọi tên ảnh đúng quy ước, ngày một cách viết, camera F/B đúng, **mã xe thiếu suy ra có lý do**. Mã: `D1, D4`.
- **5 — Sequence.** Phát hiện đủ chỗ trùng mã, cấp mã mới theo quy tắc, mỗi sequence thuộc đúng một (xe, ngày, camera), `seq_remap.csv` giải thích. Mã: `D2, D3`.
- **3 — Đổi tên không phá file nhãn.** `file_name` trong nhãn khớp tên mới (`B4`), có `rename_map.csv` chạy lại được.
- **2 — Drills.** 4 bài luyện đúng, lập luận ngắn.

## 3. Đóng gói lô (20)
- **6 — Đủ bốn phần, đúng cấu trúc.** Mã: `A1–A7`. *Mất điểm:* file lạ trong lô, thiếu `ATTRIBUTION.csv` (Track B), tên file nhãn sai phiên bản.
- **5 — Manifest và hash.** `manifest.csv` đúng từng file và sha256; zip tái lập được; hash ghi trong phiếu. Mã: `C1–C3, F4`. *Hiểu:* hash chứng minh gì / không chứng minh gì.
- **5 — README.txt và `qc_report.txt`.** Đủ 9 mục, số khớp thật, kết luận Release/Hold/Rework kèm mẫu số **theo đúng ngưỡng Day 7**. Với bộ Track B: đáp án chuẩn là *vòng 1 39/40 = 97,5% ⇒ Rework; đã sửa và kiểm lại ⇒ kết luận cuối Release*, ghi **cả hai vòng** (đủ điểm); chỉ ghi 40/40 mà bỏ vòng 1 (một nửa); Release không có số liệu đạt (0 và bị trừ nặng). Mã: `E1–E12`.
- **4 — `label_summary.csv` và đối soát CVAT.** Từng lớp khớp, dòng TOTAL đúng. Mã: `B9–B11`.
- Trừ nặng: kết luận Release khi tỉ lệ đạt cuối < 98% (`E12` FAIL); số ảnh/số nhãn bịa.

## 4. Truy vết và phân tích tác động (20)
- **6 — `truyvet.csv`.** Mỗi ảnh một dòng, đúng nguồn (assignee → job → ảnh; phiếu QC; header job), người kiểm khác người gán. Mã: `D5–D8`. *Mất điểm:* chép chung chung một giá trị cho mọi ảnh, sai job.
- **4 — Chia tập không rò rỉ.** `split.csv` chia theo sequence (`D9`); trong `impact_analysis.md` có số sequence rò khi chia theo frame và **giải thích bằng lời của bạn**.
- **7 — Khoanh vùng** (đáp án Track B do giảng viên giữ; định nghĩa ở GUIDE 4.2): tầng (a) đúng và đủ ảnh (2 điểm); tầng (b) đúng theo **tiêu chí bạn nêu rõ** và nhất quán với `truyvet.csv` (2 điểm); báo đúng người gán/kiểm cho từng nhóm (2 điểm); so sánh "có truy vết vs không có" bằng số của lô bạn (1 điểm).
- **3 — Lô sửa.** Tên `lo_NNN_v2` (`G-v2`), nói rõ **không ghi đè v1**, thay đổi gì, README/manifest/hash cập nhật thế nào.
- Trừ nặng: liệt kê ảnh không lọc theo guideline, bỏ sót người cần báo, đề xuất ghi đè v1.

## 5. Bảo mật (10)
- **4 — Tình huống.** Ca USB, ca 5 việc được/không, ca khuôn mặt (kết luận **Hold + báo người phụ trách**, không tự xử lý). Mã: `F7, F8`.
- **3 — Phân quyền và NDA** gắn với việc bạn **vừa làm** (đóng vai Quản trị xuất lô; quyền tối thiểu; cái gì là thông tin mật).
- **3 — Tự soi dữ liệu của mình:** `prompts.md` có lộ dữ liệu thật không; lô có được phép lên repo public không (giấy phép, ảnh riêng tư). *Mất điểm:* bài trả lời copy slide, không liên hệ bài làm.

## 6. Trung thực, tái lập, quy trình (15)
- **5 — Bộ kiểm.** `check_batch.py` không còn FAIL; `receive_batch.py` không còn câu hỏi. Bằng chứng: output chạy lại của người chấm trên bản sao sạch của `scripts/`.
- **4 — Lịch sử commit.** ≥ 7 commit mang tên bạn, mỗi pha một commit, thứ tự hợp lý (xem RULES). Không commit `*.zip`, `work/`, secret.
- **3 — Dùng AI minh bạch.** `prompts.md` đủ prompt, bản trả lời, **chỗ bạn sửa**; không dán dữ liệu thật.
- **3 — `individual_note.md`.** Trả lời câu "PASS có nghĩa nhãn đúng không", bài học cụ thể, một điều làm khác lần sau; (nếu có) kết quả đổi lô với bạn.

## Trừ điểm chung
- Thiếu thành phần: chỉ chấm phần có bằng chứng.
- **Số liệu giả** (nhãn, QC, hash, người gán/kiểm bịa): 0 điểm phần liên quan, báo giảng viên.
- Sửa `scripts/` hoặc `data/starter/` để qua bộ kiểm: 0 điểm hạng mục 6. Người chấm chạy `check_batch.py` bản **gốc** của giảng viên trên `submission/` của bạn.
- Nộp muộn, sai tên repo, sai link: theo [RULES.md](RULES.md).
