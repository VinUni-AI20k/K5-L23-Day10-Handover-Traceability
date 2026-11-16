# Submission — bài cá nhân

## Repo bài nộp

Mỗi học viên **một repo public** (fork/clone từ repo đề), đặt tên theo mẫu:

| Mẫu tên repo | Ví dụ |
|---|---|
| `K5-L23-DAY10-[MSHV]-[HoTen]-Handover` | `K5-L23-DAY10-22001234-NguyenVanA-Handover` |

`HoTen` không dấu, viết liền.

Theo hướng dẫn lớp nếu giảng viên đặt quy ước khác.

## Trước khi nộp

1. **Đổi dòng tiêu đề của `README.md`:**
   ```markdown
   # Day 10 Lab — 22001234 - Nguyễn Văn A
   ```
2. Điền [STUDENT.md](STUDENT.md) (kể cả "Kết quả tóm tắt").
3. `python scripts/check_submission.py` (= `check_batch.py`) không còn `FAIL`.
4. Nộp link repo lên LMS **https://aithucchien.vinuni.edu.vn** hoặc kênh giảng viên/coach chỉ định.

## Cấu trúc bắt buộc

```text
README.md                          # dòng đầu: # Day 10 Lab — <MSHV> - <Họ và tên>
STUDENT.md                         # thông tin + kết quả tóm tắt
lab_config.json                    # đã điền
submission/
├── lo_NNN_v1/                     # THƯ MỤC LÔ BÀN GIAO
│   ├── images/                    # ảnh đã đổi tên theo quy ước (có thể vắng nếu dữ liệu riêng tư, xem RULES)
│   ├── annotations/instances_v1.json
│   ├── manifest.csv
│   ├── label_summary.csv
│   ├── qc_report.txt
│   ├── README.txt
│   ├── truyvet.csv
│   └── ATTRIBUTION.csv            # có cột new_name; Track B bắt buộc
├── lo_NNN_v1.sha256               # mã băm của lo_NNN_v1.zip (KHÔNG commit zip)
├── phieu_ban_giao.md
├── security.md
├── individual_note.md
├── worklog/
│   ├── kiem_lo.py                 # TỰ VIẾT
│   ├── prompts.md
│   ├── mutation_test.md
│   ├── cvat_counts.csv
│   ├── check_report_export1.txt
│   ├── check_report_export2.txt
│   ├── fixture_clean.json, fixture_images/, mutants/   # mutation test (3 bản hỏng)
│   ├── export_1/, export_2/       # Track A
│   ├── bug_ticket.md
│   ├── rename_map.csv
│   └── seq_remap.csv
└── analysis/
    ├── split.csv
    └── impact_analysis.md
```

`NNN` = 3 chữ số cuối MSHV. Không commit `*.zip`, thư mục `work/`, secret. Không sửa `scripts/`, `data/starter/`.

## Checklist trước khi nộp (5 mục của slide + mục của lab)

Năm mục bàn giao cũng nằm cuối `phieu_ban_giao.md`; phải tự tích sau khi **đã kiểm thật**:

- [ ] **Đủ bốn phần của lô**: danh sách file, số nhãn, phiên bản guideline, báo cáo QC.
- [ ] **File xuất qua bốn câu kiểm**: mở lại được, đúng tên lớp, đủ số nhãn, đúng định dạng.
- [ ] **Metadata đủ bốn trường**: scene/sequence, xe, ngày, camera.
- [ ] **Truy vết**: người gán, người kiểm, guideline cho từng ảnh.
- [ ] **Dữ liệu ở lại hệ thống**: không USB, email cá nhân, chatbot với dữ liệu thật.

Thêm của lab:

- [ ] Repo public, tên đúng quy tắc, mở được khi chưa đăng nhập.
- [ ] Tiêu đề `README.md` đã đổi.
- [ ] `kiem_lo.py` tự viết, có `mutation_test.md` (3 lỗi cài).
- [ ] `bug_ticket.md` commit **trước** khi dùng export lần 2 (Track B).
- [ ] Kết luận Release/Hold/Rework **khớp số liệu** và nhất quán ở README, `qc_report.txt`, phiếu.
- [ ] `receive_batch.py` không còn câu hỏi; hash trong phiếu = `lo_NNN_v1.sha256`.
- [ ] ≥ 5 commit của bạn, mỗi pha một commit.
- [ ] Đã nộp link trước hạn.
