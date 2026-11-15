# Hướng dẫn làm lab (từng pha)

Bài **cá nhân**, dự kiến **4,5 giờ (270 phút)**: 4 giờ tại lớp cho P0–P5 nếu bạn làm đều tay, phần còn lại cho P6 và sửa lỗi. Mốc tự kiểm tra: [CHECKPOINTS.md](CHECKPOINTS.md). Chấm điểm: [RUBRIC.md](RUBRIC.md). Kiến thức: [docs/HANDOVER_CHEATSHEET.md](docs/HANDOVER_CHEATSHEET.md).

```
Pha 0  Chuẩn bị, chọn track                 (~15')
Pha 1  Kiểm file xuất                       (~70')   tự viết script, đối soát CVAT, báo lỗi
Pha 2  Metadata và đổi tên                  (~50')
Pha 3  Đóng gói lô, truy vết, phiếu         (~65')
Pha 4  Chia tập và xử lý báo lỗi            (~35')
Pha 5  Bảo mật                              (~15')
Pha 6  Kiểm cuối, nhận lô                   (~20')
```

> **Quy ước.** `NNN` = 3 chữ số cuối MSHV (22001234 → `234`); lô của bạn tên `lo_234_v1`. Mã người nộp của bạn: 1 chữ cái + 2 chữ số (ví dụ `S34`).

## Cách gõ lệnh (đọc trước)

Mọi lệnh chạy **từ thư mục gốc repo**, **trên một dòng** (trong GUIDE vài lệnh dài chia dòng cho dễ đọc: hãy nối lại).

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Gọi Python | `python3` | `py` (nếu không có thì `python`) |
| Nối hai lệnh | `a && b` | chạy từng lệnh riêng (PowerShell 5 không có `&&`) |
| Ghi output ra file | để chương trình tự ghi (`--out`) | như bên trái; **đừng dùng `>`** (dễ lỗi font hoặc UTF-16) |
| Đường dẫn | `submission/worklog/x` | `submission\worklog\x` hoặc `/` đều chạy |

Trong GUIDE, `python` nghĩa là lệnh gọi Python 3.9+ trên máy bạn (chạy `python3 --version` hoặc `py --version` để biết cái nào dùng được). Nếu có chữ tiếng Việt in ra lỗi font trên Windows, thêm `-X utf8`: `py -X utf8 scripts/check_batch.py`.

## Tóm tắt một trang

| Pha | Việc | Lệnh chính | Sản phẩm (trong `submission/`) |
|---|---|---|---|
| 0 | Clone, điền cấu hình | | `lab_config.json` (ở gốc repo) |
| 1 | Viết script kiểm, kiểm export, đối soát, báo lỗi | `kiem_lo.py` (bạn viết) | `worklog/kiem_lo.py`, `check_report_export1.txt`, `cvat_counts.csv`, `bug_ticket.md`, `mutation_test.md`, `prompts.md`, `check_report_export2.txt` |
| 2 | Chuẩn hoá metadata, đổi tên | `check_names.py`, `apply_rename.py` | `worklog/rename_map.csv`, `seq_remap.csv`, `drills.md`, `lo_NNN_v1/images`, `annotations`, `ATTRIBUTION.csv` |
| 3 | Đóng gói đủ bốn phần + truy vết | `build_manifest.py`, `build_label_summary.py`, `pack_batch.py`, `receive_batch.py` | `lo_NNN_v1/*`, `truyvet.csv`, `lo_NNN_v1.sha256`, `phieu_ban_giao.md` |
| 4 | Chia tập, xử lý báo lỗi | `make_split.py`, `trace_query.py` | `analysis/split.csv`, `analysis/impact_analysis.md` |
| 5 | Bảo mật | (viết) | `security.md` |
| 6 | Kiểm cuối | `check_batch.py`, `receive_batch.py` | `individual_note.md` |

Nhiều file mẫu đã đặt sẵn trong `submission/` với chỗ `<<...>>` để điền; `check_batch.py` báo `FAIL` nếu còn sót. Mẫu cho file nằm trong lô: [docs/templates/](docs/templates/).

---

## Pha 0 — Chuẩn bị (15 phút)

```bash
git clone <repo của bạn>
cd <repo>
```
1. Sửa `lab_config.json`:
   ```json
   {
     "mshv": "22001234", "ho_ten": "Nguyen Van A", "track": "B",
     "batch_id": "lo_234_v1", "submitter_code": "S34",
     "classes": ["car", "truck", "van", "motorcycle", "person"]
   }
   ```
   `track` là `"A"` hoặc `"B"` (chữ hoa). Tên lớp trong `classes` là **chuẩn**: mọi so khớp sau khớp từng ký tự với danh sách này.
   Tuỳ chọn (xem [data/README.md](data/README.md)): `"images_dir"` (Track A: thư mục ảnh gốc), `"images_private": true`, `"allow_same_reviewer": true`.
2. Đọc [docs/HANDOVER_CHEATSHEET.md](docs/HANDOVER_CHEATSHEET.md) một lượt.
3. **Track A:** gom đủ bộ giấy tờ tương đương starter theo bảng ở [data/README.md](data/README.md). Thiếu thì **dừng và hỏi coach**.
4. Commit: `git add -A` rồi `git commit -m "P0: cau hinh"` (hai lệnh riêng). Mỗi pha một commit: lịch sử commit cũng là truy vết.

---

## Pha 1 — Kiểm file xuất trước khi nộp (70 phút)

Bốn câu phải trả lời **Có**: *mở lại được · đúng tên lớp · đủ số nhãn · đúng định dạng*. Bạn tự viết công cụ để trả lời chúng.

**File xuất lần 1**
- Track B: `data/starter/cvat_export_1/annotations/instances_default.json`, ảnh ở `data/starter/images/`.
- Track A: file COCO 1.0 bạn export (xem [docs/CVAT_EXPORT.md](docs/CVAT_EXPORT.md)), đặt ở `submission/worklog/export_1/annotations/instances_default.json`; ghi `"images_dir"` trong `lab_config.json`.

> **Track B:** chưa mở `cvat_export_2_reexport/` cho tới bước 1.6.

### 1.1 Số nhãn theo CVAT (10 phút)
Ghi `submission/worklog/cvat_counts.csv` (cột `class,cvat_count`, mỗi lớp một dòng; tên lớp là tên **chuẩn**). Track B: **cộng các job** trong `data/starter/cvat_info/jobs.csv` (đó là số bạn chép từ Info của từng job); Track A: mở từng job → **Info** (xem tài liệu CVAT).
```csv
class,cvat_count
car,12
```
(Ví dụ số giả.)

### 1.2 Viết `kiem_lo.py` (25 phút) — bạn tự viết
File: `submission/worklog/kiem_lo.py`, chỉ thư viện chuẩn, **không import** từ `scripts/` (bộ kiểm bắt). Giao diện cố định, vì bộ kiểm sẽ **chạy lại** script của bạn:

```
python submission/worklog/kiem_lo.py <file_nhan.json> <thu_muc_anh> --classes car truck van motorcycle person --cvat-counts submission/worklog/cvat_counts.csv --out <file_bao_cao.txt>
```
Phải làm đủ 7 việc, vừa in màn hình vừa ghi **UTF-8** vào `--out`:
1. số ảnh, số nhãn; số nhãn **theo từng tên lớp đúng như ghi trong file** (không chuẩn hoá);
2. tên lớp không thuộc `--classes`, in bằng `repr` để thấy dấu cách thừa;
3. **tên từng ảnh** có trong file nhãn mà thiếu file ảnh, và ngược lại (file ảnh không có trong nhãn). Bỏ qua file ẩn như `.DS_Store`, `Thumbs.db`;
4. **id từng nhãn** có box nằm ngoài ảnh; **id từng nhãn** có box rộng hoặc cao ≤ 0;
5. đối soát số nhãn từng lớp với `cvat_counts.csv`: lớp nào lệch, lệch bao nhiêu (lưu ý: lớp tên sai chưa tính vào lớp chuẩn);
6. dòng cuối `KẾT LUẬN: ĐẠT` hoặc `KẾT LUẬN: KHÔNG ĐẠT`; thoát mã 1 nếu không đạt, mã 0 nếu đạt;
7. **không sửa file nào**.

Được dùng AI (xem [RULES.md](RULES.md)) nhưng: ghi prompt vào `worklog/prompts.md`; prompt chỉ có **3 dòng dữ liệu giả**; bạn phải đọc hiểu từng dòng và ghi **bạn đã sửa gì** trong code AI viết. Có thể bị hỏi vấn đáp về một dòng bất kỳ.

### 1.3 Chứng minh script bắt được lỗi (15 phút)
Script im lặng không có nghĩa là file sạch. Dùng mẫu [docs/templates/fixture_clean.json](docs/templates/fixture_clean.json) (3 ảnh, 5 box) copy thành `submission/worklog/fixture_clean.json`; tạo thư mục `submission/worklog/fixture_images/` với 3 file ảnh giả `f1.jpg f2.jpg f3.jpg` (file bất kỳ, đổi tên); và một `cvat_counts` riêng cho fixture. Tự tạo **≥ 5 bản hỏng** (một lỗi mỗi bản): tên lớp `Car`; tên lớp dấu cách thừa; thiếu một ảnh; box ngoài ảnh; box rộng 0; nhãn ít hơn CVAT. Chạy script trên từng bản, ghi bảng **lỗi cài / có bắt không / dòng output** vào `submission/worklog/mutation_test.md`. Bản hỏng lưu trong `submission/worklog/mutants/` (commit). Script bỏ sót lỗi nào thì **sửa script** và ghi lại.

### 1.4 Kiểm export lần 1 (5 phút)
```
python submission/worklog/kiem_lo.py <export_1.json> <thu_muc_anh> --classes car truck van motorcycle person --cvat-counts submission/worklog/cvat_counts.csv --out submission/worklog/check_report_export1.txt
```
(Track B: `<export_1.json>` = `data/starter/cvat_export_1/annotations/instances_default.json`, `<thu_muc_anh>` = `data/starter/images`.) Báo cáo này phải là **output thật** của script: bộ kiểm chạy lại và so.

### 1.5 Báo lỗi — `bug_ticket.md` (10 phút)
Điền `submission/worklog/bug_ticket.md`: từng lỗi (loại, số lượng, **tên lớp sai viết `repr`, id nhãn, tên ảnh**), **hệ quả với team AI** ("hai ảnh thiếu có thể gây ra điều gì?"), việc cần người quản trị làm **trong CVAT** (không sửa tay JSON). Bộ kiểm đối chiếu: mọi tên lớp sai, mọi id box lỗi, mọi ảnh thiếu mà script thấy ở export_1 đều phải xuất hiện trong ticket.
Chênh dù **một nhãn** cũng phải giải thích: nhãn mất thuộc ảnh nào (gợi ý: so danh sách ảnh của job với ảnh trong file xuất; và nhớ bước 5 của 1.2 trừ nhãn tên sai ra khỏi lớp chuẩn).
**Commit `bug_ticket.md` trước khi làm 1.6.**

### 1.6 File xuất lần 2 (5 phút)
Người quản trị sửa trong CVAT theo báo lỗi rồi xuất lại.
- Track B: bây giờ mới mở `data/starter/cvat_export_2_reexport/`.
- Track A: tự sửa trong CVAT rồi export lại vào `submission/worklog/export_2/annotations/instances_default.json`. Nếu lô của bạn thật sự sạch: **không cài lỗi vào dữ liệu thật**; ghi "0 lỗi" trong ticket kèm bằng chứng (báo cáo export_1 ĐẠT, nhập lại CVAT thành công) và dùng `mutation_test.md` làm bằng chứng script có năng lực bắt lỗi (xem [RUBRIC.md](RUBRIC.md), bảng Track A); `export_2` = bản sao `export_1`.

Chạy lại `kiem_lo.py` → `check_report_export2.txt` phải kết luận **ĐẠT**.
**Nhập lại CVAT (Track A bắt buộc, Track B tuỳ chọn):** task mới cùng ảnh/lớp → *Upload annotations* đúng format, chọn **Replace** (Append cộng thêm nhãn). Ghi 2–3 dòng kết quả vào cuối `bug_ticket.md`.

**Tự hỏi:** script PASS có nghĩa nhãn đúng không? (Ghi câu trả lời vào `individual_note.md`.)

---

## Pha 2 — Metadata và đổi tên (50 phút)

Mẫu tên: `vehNN_YYYYMMDD_camX_seqNNN_NNNNNN.jpg` (X ∈ F,B,L,R). Ngày: `2026-11-05` trong CSV, `20261105` trong tên file.

### 2.1 Luyện nhanh (10 phút) — `submission/worklog/drills.md`
Năm bài của slide: tìm lỗi 6 tên file; ghi metadata thành tên; hash đổi một ký tự; khoanh vùng 4 ảnh theo bảng người gán/guideline; **chấm lô mẫu `final_moi.zip`** (≥ 4 điểm chưa đạt và cách sửa). Làm trước, rồi kiểm lại bằng `python scripts/check_names.py <tên>...` và `python scripts/hash_file.py thu.txt`.

### 2.2 Chuẩn hoá metadata (25 phút)
Nguồn: Track B `data/starter/capture_log.csv` (đọc `capture_log_README.md` trước); Track A nhật ký/tên gốc/nguồn của bạn. Đọc gợi ý ở [docs/templates/normalize_hints.md](docs/templates/normalize_hints.md) (cách đọc ngày nhiều kiểu, ánh xạ camera): tự quyết dùng script hay bảng tính.
1. `submission/worklog/rename_map.csv` (cột `old_name,new_name`, mỗi ảnh một dòng, **dấu phẩy**; Excel vi-VN hay lưu `;`: chọn *CSV UTF-8 (Comma delimited)*).
2. **Sequence trùng mã.** Mã sequence phải **duy nhất toàn lô**. Quy tắc cấp mã mới: xử lý các đoạn thu theo thứ tự **ngày tăng dần; cùng ngày thì theo tên ảnh gốc đầu tiên của đoạn**. Đoạn nào có mã đã bị đoạn *trước đó* (xe hoặc ngày khác) dùng thì nhận mã mới = **số lớn nhất đang dùng trong lô + 1**, rồi mã đó coi là đã dùng (đoạn sau nhận tiếp +1). Ghi `submission/worklog/seq_remap.csv`: `old_seq,new_seq,vehicle,date,reason`; không có trùng thì để đúng dòng tiêu đề và nói rõ trong `drills.md`.
3. Dòng thiếu mã xe: suy từ ảnh cùng đoạn (cùng ngày, camera, sequence), **ghi lý do**.
4. Track A, nguồn không có xe/camera/sequence: tự đặt mã **nhất quán và giải thích** trong README Ghi chú. Sequence = **một lần chụp liên tục** (cùng tác giả/cùng sự kiện/cùng phiên gán, theo `ATTRIBUTION.csv` hoặc ghi chú nguồn), **không** mỗi ảnh một sequence (như thế chia tập mất ý nghĩa).

### 2.3 Đổi tên + sửa file nhãn (10 phút)
```
python scripts/apply_rename.py --map submission/worklog/rename_map.csv --src-images data/starter/images --src-annotations data/starter/cvat_export_2_reexport/annotations/instances_default.json --attribution data/starter/ATTRIBUTION.csv
```
(Track A đổi ba đường dẫn nguồn.) Tạo `submission/lo_NNN_v1/images/`, `annotations/instances_v1.json` (sửa `file_name` cho khớp tên mới) và `ATTRIBUTION.csv` (có thêm cột `new_name`; bản gốc khoá theo tên cũ nên team AI không ghép được).

---

## Pha 3 — Đóng gói lô, truy vết, phiếu bàn giao (65 phút)

Lô đủ **bốn phần**: danh sách file · số nhãn · phiên bản guideline · báo cáo QC. Thiếu một phần thì lô chưa được coi là bàn giao.

```
submission/lo_NNN_v1/
├─ images/            ├─ manifest.csv          ├─ qc_report.txt
├─ annotations/       ├─ label_summary.csv     ├─ README.txt
│  └ instances_v1.json├─ truyvet.csv           └─ ATTRIBUTION.csv
```

1. `python scripts/build_manifest.py` rồi `python scripts/build_label_summary.py`. Đọc hai file: `label_summary.csv` phải khớp `cvat_counts.csv`.
2. **`truyvet.csv`** (một dòng mỗi ảnh, **tên mới**): `image,annotator,reviewer,guideline`. Ba câu cho mỗi ảnh: ai gán, ai kiểm, guideline nào. Ghép từ ba nguồn (CVAT **không** tự ghi người kiểm và guideline):

   | Cột | Lấy từ | Track B | Track A |
   |---|---|---|---|
   | `annotator` | người được giao job | `cvat_info/jobs.csv` (khoảng ảnh của job) | Job → Assignee trong CVAT |
   | `reviewer` | phiếu QC của job | `qc_forms/qc_job_*.txt` | phiếu QC Day 7/9 |
   | `guideline` | phiên bản ghi ở đầu job | `cvat_info/job_headers.txt` | ghi chú đầu job, hoặc v1.0/v1.1 của Day 7 |

   Tên mã người: `A07`, `Q03` (1 chữ + 2 chữ số). Track A dùng **mã giả danh**; bảng ánh xạ tên thật ↔ mã **không commit**. Người kiểm khác người gán; nếu thật sự không có người kiểm độc lập, đặt `"allow_same_reviewer": true` và giải thích trong README Ghi chú (bị trừ một phần điểm hạng mục 4).
3. **`qc_report.txt`** — mẫu [docs/templates/qc_report_template.txt](docs/templates/qc_report_template.txt). Lấy số từ phiếu QC. Ghi **mọi vòng** kèm **mẫu số**. Quy tắc kết luận (Day 7): > 2% ảnh lỗi ở một vòng ⇒ vòng đó là **Rework** (sửa rồi kiểm lại); nếu sau sửa kiểm lại đạt ≥ 98% thì **kết luận cuối của lô là Release**, nhưng phải ghi rõ vòng 1 và việc đã kiểm lại ảnh nào (kiểm lại *chỉ ảnh đã sửa* chỉ chấp nhận khi phiếu QC ghi như vậy). Dòng `Kết luận:` bắt đầu bằng đúng một từ `Release`, `Rework` hoặc `Hold`.
4. **`README.txt`** — mẫu [docs/templates/README_TEMPLATE.txt](docs/templates/README_TEMPLATE.txt). Dòng `QC:` **kết thúc bằng `- Release` (hoặc Rework / Hold)** = kết luận cuối. Số ảnh, số nhãn phải khớp thật. Soạn bằng trình soạn thảo văn bản thuần (Notepad, VS Code; macOS: TextEdit → *Make Plain Text*), lưu UTF-8.
5. **Đóng gói và hash** (chỉ khi mọi file trong lô đã chốt): `python scripts/pack_batch.py` → `submission/lo_NNN_v1.zip` (không commit) và `submission/lo_NNN_v1.sha256` (commit).
6. **Phiếu bàn giao:** điền `submission/phieu_ban_giao.md` (8 dòng + checklist 5 mục), dán SHA-256. Dòng `Kết luận:` bắt đầu bằng đúng một từ khoá.
7. **Nhận lô như team AI:** `python scripts/receive_batch.py submission/lo_NNN_v1.zip submission/lo_NNN_v1.sha256`. Phần "CÂU HỎI CÒN PHẢI HỎI LẠI" phải **trống**; còn thì sửa lô, đóng gói lại, cập nhật hash trong phiếu.

> Đổi bất kỳ file nào trong lô sau bước 5 ⇒ `build_manifest.py` (nếu đổi ảnh/nhãn) → `pack_batch.py` → cập nhật phiếu. **Không ghi đè lô đã nộp**: bản sửa là `lo_NNN_v2`.

---

## Pha 4 — Chia tập và xử lý báo lỗi của team AI (35 phút)

### 4.1 Chia train / val không rò rỉ (10 phút)
```
python scripts/make_split.py --by frame --seed 1
python scripts/make_split.py --by sequence --seed 1
```
Chạy cách **sai** trước, chép dòng kết quả (số sequence rò) vào `impact_analysis.md` mục 6, rồi chạy cách **đúng** để `submission/analysis/split.csv` cuối cùng là bản đúng. Giải thích bằng lời của bạn: vì sao chia theo frame làm điểm đánh giá "cao giả"? Vì sao sequence ID **phải duy nhất toàn lô** (liên hệ `seq_remap.csv`)? Nếu cảnh báo "lệch tỉ lệ" xuất hiện, nêu nguyên nhân.

### 4.2 Team AI báo lỗi (25 phút)
- Track B: đọc `data/starter/incoming/team_ai_ticket.md` và `guideline/changelog.md`. (`lo_900` trong ticket là tên giả định của lô starter; lô của bạn là `lo_NNN_v1`.)
- Track A: tự dựng một báo lỗi có thật trong dữ liệu của bạn từ một quy tắc đã đổi v1.0 → v1.1 ở Day 7; ghi nguyên văn trong `impact_analysis.md` mục 1; coach chấm theo tính nhất quán với `truyvet.csv` của bạn và vấn đáp.

Dùng `truyvet.csv` và `python scripts/trace_query.py ...` để trả lời trong `submission/analysis/impact_analysis.md`:
1. **Tầng (a):** ảnh đúng như team AI báo = ảnh thuộc các sequence được nêu, gán theo **phiên bản guideline cũ** (trước khi đổi), và có nhãn của **lớp bị đổi quy tắc**.
2. **Tầng (b), rủi ro hệ thống:** các ảnh khác (ngoài tầng a) cũng gán theo phiên bản cũ và cũng có nhãn lớp bị đổi, dù chưa ai báo. Lưu ý: tiêu chí dùng *phiên bản ghi ở job*, không dùng ngày chụp ảnh. Nhãn Track B là tổng hợp nên "ảnh có nhãn lớp đó" là **tiêu chí đại diện**: ghi rõ bạn dùng tiêu chí nào.
3. Báo ai (người gán, người kiểm của từng nhóm ảnh)?
4. Lô sửa tên gì (`lo_NNN_v2`), đổi gì, giữ gì, README/manifest/hash cập nhật thế nào (**không ghi đè v1**).
5. So sánh: có `truyvet` thì mở lại bao nhiêu ảnh trên tổng bao nhiêu; không có thì sao.
6. Chia tập (4.1).

Liệt kê **tên ảnh đầy đủ**. Bạn không cần sửa nhãn, chỉ phân tích và lập kế hoạch.

---

## Pha 5 — Bảo mật khi làm việc (15 phút)

Điền `submission/security.md` (7 mục có sẵn): ba nguyên tắc, phân quyền (bạn đóng vai Quản trị khi xuất/đóng gói lô), ca USB, bảng 5 việc, **ca khuôn mặt (kết luận Hold)**, tự soi dữ liệu của chính bạn (prompt có lộ dữ liệu thật không; ảnh nào có mặt người/biển số đọc được trong lô và vì sao vẫn dùng được cho lab; giấy phép), NDA. Mục khuôn mặt phải có tiêu đề chứa chữ "khuôn mặt".
Track A dữ liệu riêng tư: **không commit ảnh**; đặt `"images_private": true`, giải thích ở `security.md` mục 6 (hash và manifest vẫn nộp được).

---

## Pha 6 — Kiểm cuối, nhận lô, tự đánh giá (20 phút)

```
python scripts/pack_batch.py
python scripts/check_batch.py
python scripts/receive_batch.py submission/lo_NNN_v1.zip submission/lo_NNN_v1.sha256
```
1. Sửa mọi `FAIL`; `WARN` đọc và quyết định.
2. Điền `submission/individual_note.md`.
3. **Tuỳ chọn:** đổi zip + mã hash với một bạn cùng lớp, chạy `receive_batch.py` trên lô của họ; ghi họ còn phải hỏi gì.
4. Đổi tiêu đề `README.md` (xem [SUBMISSION.md](SUBMISSION.md)), commit, push, nộp link.

## Lỗi hay gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `check_batch` B4: ảnh trong nhãn khác `images/` | Quên `apply_rename.py`, hoặc đổi tên ảnh bằng tay nên `file_name` trong nhãn vẫn tên cũ. |
| C2: sha256 khác | Bạn sửa ảnh/nhãn sau khi lập manifest: chạy lại `build_manifest.py`. |
| C3: zip không khớp | Sửa lô sau khi đóng gói: `pack_batch.py` lại, cập nhật phiếu. |
| D2: sequence trùng mã | Xem Pha 2.2 bước 2. |
| G-own | `kiem_lo.py` import từ `scripts/`: tự viết lại. |
| G-run1: không có `--out` | Thêm tham số `--out` vào `kiem_lo.py` (Pha 1.2). |
| G-rep1: báo cáo khác output thật | Chạy lại 1.4 để ghi báo cáo, đừng sửa tay. |
| G-ticket: thiếu chi tiết | `bug_ticket.md` phải nêu mọi tên lớp sai, id box lỗi, ảnh thiếu như script báo. |
| README mục E9 | Dòng `QC:` phải kết thúc bằng ` - Release` / Rework / Hold. |
| Zip hai máy khác nhau | Dùng `pack_batch.py`, không dùng "Compress" của hệ điều hành; file ẩn (`.DS_Store`) được tự bỏ. |
| `git` đổi dấu xuống dòng | Repo có `.gitattributes` ép LF cho `.txt/.csv/.json/.md`; đừng tắt. |
