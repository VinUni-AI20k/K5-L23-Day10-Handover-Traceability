"""Sinh hình minh hoạ (sơ đồ, KHÔNG phải ảnh chụp màn hình) cho README. Giảng viên dùng; học viên không cần chạy.

    python docs/assets/make_figures.py
Cần Pillow. Đầu vào: data/starter/images/*.jpg. Đầu ra: hero.png, roadmap.png, sample_grid.jpg, batch_anatomy.png.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FONTS = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"]
FONTS_B = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"]
NAVY, TEAL, ORANGE, GREEN, RED, PURPLE, GRAY, LIGHT = "#0b1f3a", "#12b3a8", "#ff8a3d", "#2fbf71", "#e5484d", "#7b61ff", "#6b7686", "#f3f6fa"


def font(size, bold=False):
    for p in (FONTS_B if bold else FONTS):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rrect(d, box, r=16, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def center(d, xy, text, f, fill="white"):
    w = d.textlength(text, font=f)
    d.text((xy[0] - w / 2, xy[1]), text, font=f, fill=fill)


def hero():
    W, H = 1600, 420
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    imgs = sorted((ROOT / "data/starter/images").glob("*.jpg"))[:6]
    for i, p in enumerate(imgs):
        t = Image.open(p).convert("RGB").resize((200, 140))
        im.paste(t, (900 + (i % 3) * 215, 60 + (i // 3) * 160))
    d.text((60, 70), "Day 10 Lab", font=font(34), fill=TEAL)
    d.text((60, 120), "Bàn giao dữ liệu", font=font(64, True), fill="white")
    d.text((60, 200), "& Truy vết", font=font(64, True), fill=ORANGE)
    d.text((60, 300), "Một lô nhãn dùng được ngay, truy vết được tới từng ảnh.", font=font(26), fill="#c9d4e2")
    im.save(HERE / "hero.png")


def roadmap():
    steps = [("P1", "Kiểm file xuất", "script tự viết, báo lỗi", GREEN), ("P2", "Chuẩn hoá + đóng gói", "đổi tên, truy vết, QC", ORANGE),
             ("P3", "Chia tập + báo lỗi", "ảnh cần sửa (tầng a/b)", RED), ("P4", "Bảo mật + kiểm cuối", "hash, nhận lô như team AI", NAVY)]
    W, H = 1600, 300
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    bw, gap = 320, 70
    x0 = (W - (4 * bw + 3 * gap)) // 2
    for i, (a, b, c, col) in enumerate(steps):
        x = x0 + i * (bw + gap)
        rrect(d, (x, 70, x + bw, 230), 18, fill=col)
        center(d, (x + bw / 2, 85), a, font(30, True))
        center(d, (x + bw / 2, 135), b, font(24, True))
        center(d, (x + bw / 2, 172), c, font(18))
        if i < 3:
            d.polygon([(x + bw + gap - 8, 150), (x + bw + 8, 133), (x + bw + 8, 167)], fill=GRAY)
    im.save(HERE / "roadmap.png")


def anatomy():
    W, H = 1600, 520
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    d.text((40, 24), "Một lô bàn giao gồm bốn phần", font=font(34, True), fill=NAVY)
    parts = [("Danh sách file", "manifest.csv", "tên từng ảnh, nhãn, sha256", TEAL), ("Số lượng nhãn", "label_summary.csv", "tổng và theo từng lớp", ORANGE),
             ("Phiên bản guideline", "README.txt + truyvet.csv", "gán theo luật nào, ảnh nào", PURPLE), ("Báo cáo QC", "qc_report.txt", "mẫu, tỉ lệ đạt, kết luận", GREEN)]
    for i, (t, f, s, col) in enumerate(parts):
        x = 40 + i * 385
        rrect(d, (x, 100, x + 360, 300), 18, fill="white", outline=col, width=4)
        d.rectangle((x, 100, x + 360, 150), fill=col)
        center(d, (x + 180, 108), t, font(24, True))
        center(d, (x + 180, 185), f, font(22, True), NAVY)
        center(d, (x + 180, 235), s, font(18), GRAY)
    d.text((40, 340), "Thiếu một phần thì lô chưa được coi là bàn giao.", font=font(26, True), fill=RED)
    d.text((40, 400), "Lô tốt:  lo_017_v1/ { images/, annotations/, manifest.csv, label_summary.csv, qc_report.txt, README.txt, truyvet.csv }", font=font(20), fill=NAVY)
    d.text((40, 440), "Lô xấu:  final_moi/ { anh xe (1).jpg, nhan_sua.json, nhan_sua (2).json }   ← không biết bản nào đúng", font=font(20), fill=GRAY)
    im.save(HERE / "batch_anatomy.png")


def grid():
    imgs = sorted((ROOT / "data/starter/images").glob("*.jpg"))[:12]
    cw, ch = 320, 213
    im = Image.new("RGB", (cw * 4, ch * 3), "white")
    for i, p in enumerate(imgs):
        t = Image.open(p).convert("RGB")
        t.thumbnail((cw, ch))
        im.paste(t, ((i % 4) * cw, (i // 4) * ch))
    im.save(HERE / "sample_grid.jpg", quality=85)


if __name__ == "__main__":
    hero(); roadmap(); anatomy(); grid()
    print("ok")
