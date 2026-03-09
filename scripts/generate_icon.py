"""Генерирует иконку MeetScribe (icon.ico) в src/assets/."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZES = [16, 32, 48, 64, 128, 256]
BG_COLOR = "#1A2332"
ACCENT = "#2BA5B5"
ACCENT_LIGHT = "#3DC5D5"


def draw_icon(size: int) -> Image.Image:
    """Рисует иконку заданного размера."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size  # alias

    # Круглый фон
    margin = int(s * 0.02)
    draw.ellipse(
        [margin, margin, s - margin - 1, s - margin - 1],
        fill=BG_COLOR,
    )

    # Микрофон — корпус (скруглённый прямоугольник)
    mic_w = s * 0.28
    mic_h = s * 0.38
    mic_x = (s - mic_w) / 2
    mic_y = s * 0.18
    r = mic_w * 0.45
    draw.rounded_rectangle(
        [mic_x, mic_y, mic_x + mic_w, mic_y + mic_h],
        radius=r,
        fill=ACCENT,
    )

    # Дуга-подставка (полукруг снизу микрофона)
    arc_w = s * 0.42
    arc_h = s * 0.22
    arc_x = (s - arc_w) / 2
    arc_y = mic_y + mic_h * 0.45
    line_w = max(int(s * 0.06), 2)
    draw.arc(
        [arc_x, arc_y, arc_x + arc_w, arc_y + arc_h * 2],
        start=0, end=180,
        fill=ACCENT_LIGHT, width=line_w,
    )

    # Ножка
    leg_x = s / 2
    leg_top = arc_y + arc_h
    leg_bot = leg_top + s * 0.12
    draw.line(
        [(leg_x, leg_top), (leg_x, leg_bot)],
        fill=ACCENT_LIGHT, width=line_w,
    )

    # Подставка (горизонтальная линия)
    base_w = s * 0.22
    draw.line(
        [(leg_x - base_w / 2, leg_bot), (leg_x + base_w / 2, leg_bot)],
        fill=ACCENT_LIGHT, width=line_w,
    )

    # Звуковые волны (маленькие дуги справа и слева)
    if s >= 48:
        wave_w = max(int(s * 0.04), 1)
        for side in (-1, 1):
            for i, offset in enumerate([s * 0.08, s * 0.15]):
                cx = s / 2 + side * (mic_w / 2 + offset)
                cy_top = mic_y + mic_h * 0.15
                cy_bot = mic_y + mic_h * 0.65
                wave_r = s * 0.04 + i * s * 0.03
                if side == -1:
                    draw.arc(
                        [cx - wave_r, cy_top, cx + wave_r, cy_bot],
                        start=120, end=240,
                        fill=ACCENT_LIGHT, width=wave_w,
                    )
                else:
                    draw.arc(
                        [cx - wave_r, cy_top, cx + wave_r, cy_bot],
                        start=-60, end=60,
                        fill=ACCENT_LIGHT, width=wave_w,
                    )

    return img


def main() -> None:
    output = Path(__file__).parent.parent / "src" / "assets" / "icon.ico"
    output.parent.mkdir(parents=True, exist_ok=True)

    images = [draw_icon(s) for s in SIZES]
    images[-1].save(
        str(output),
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=images[:-1],
    )
    print(f"Icon saved to {output}")


if __name__ == "__main__":
    main()
