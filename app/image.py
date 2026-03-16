"""Server-side share card image generation using Pillow."""

from PIL import Image, ImageDraw, ImageFont
import io
import os

# 2x resolution for retina
S = 2
CARD_W = 375 * S
PAD = 24 * S
INNER = 16 * S
TEXT_W = CARD_W - 2 * PAD - 2 * INNER

# Colors
BG = (250, 250, 245)
WHITE = (255, 255, 255)
INK = (30, 30, 30)
INK2 = (61, 61, 61)
MUTED = (107, 107, 107)
BORDER = (229, 224, 218)
FOOTER_C = (168, 163, 157)

RISK_COLORS = {
    "extreme": (220, 38, 38),
    "high": (233, 115, 22),
    "moderate": (245, 158, 11),
    "low": (42, 107, 107),
    "minimal": (5, 150, 105),
    "override": MUTED,
}

_TAG = {
    "high":     {"t": (220, 38, 38),  "bg": (254, 242, 242), "bd": (254, 202, 202)},
    "med_high": {"t": (233, 115, 22), "bg": (255, 247, 237), "bd": (254, 215, 170)},
    "moderate": {"t": (217, 119, 6),  "bg": (255, 251, 235), "bd": (253, 230, 138)},
    "low":      {"t": (42, 107, 107), "bg": (232, 244, 244), "bd": (167, 216, 216)},
    "safe":     {"t": (5, 150, 105),  "bg": (236, 253, 245), "bd": (167, 243, 208)},
}

_FONT_PATHS = [
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

_font_cache: dict[tuple, ImageFont.FreeTypeFont] = {}


def _font(size: int) -> ImageFont.FreeTypeFont:
    key = size
    if key in _font_cache:
        return _font_cache[key]
    for p in _FONT_PATHS:
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            _font_cache[key] = f
            return f
    f = ImageFont.load_default(size)
    _font_cache[key] = f
    return f


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            lines.append("")
            continue
        cur = ""
        for ch in para:
            test = cur + ch
            if draw.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def _tag_style(score: int) -> dict:
    if score >= 6: return _TAG["high"]
    if score >= 4: return _TAG["med_high"]
    if score == 3: return _TAG["moderate"]
    if score == 2: return _TAG["low"]
    return _TAG["safe"]


def _tag_text(score: int, zh: bool) -> str:
    if zh:
        if score >= 6: return "高危"
        if score >= 4: return "中高风险"
        if score == 3: return "中等"
        if score == 2: return "较低"
        return "安全"
    else:
        if score >= 6: return "High Risk"
        if score >= 4: return "Med-High"
        if score == 3: return "Moderate"
        if score == 2: return "Low"
        return "Safe"


def generate_share_image(result: dict, lang: str = "zh") -> bytes:
    zh = lang == "zh"
    is_override = result.get("risk_level") == "override"
    color = RISK_COLORS.get(result.get("risk_level", "moderate"), MUTED)

    # Fonts
    score_f = _font(40 * S)
    unit_f = _font(13 * S)
    job_f = _font(11 * S)
    label_f = _font(15 * S)
    title_f = _font(13 * S)
    body_f = _font(11 * S)
    tag_f = _font(10 * S)
    dim_label_f = _font(11 * S)
    footer_f = _font(10 * S)
    line_h = 16 * S

    # Pre-calculate height on scratch surface
    tmp = Image.new("RGB", (CARD_W, 1))
    d = ImageDraw.Draw(tmp)

    advice_raw = result.get("advice_zh" if zh else "advice_en", "").replace("\n\n", "\n")
    advice_lines = _wrap(d, advice_raw, body_f, TEXT_W)
    breakdown = result.get("breakdown", []) if not is_override else []

    # Vertical layout calculation
    y = 28 * S
    # score section
    y += (48 * S if is_override else 46 * S)
    y += 18 * S  # job name
    y += 26 * S  # risk label
    # advice card
    advice_h = INNER + 20 * S + len(advice_lines) * line_h + INNER
    y += advice_h + 10 * S
    # dimension card
    if breakdown:
        dim_h = INNER + 24 * S + len(breakdown) * 24 * S + 8 * S
        y += dim_h + 10 * S
    # footer
    y += 28 * S + 28 * S

    total_h = y

    # ── Draw ──
    img = Image.new("RGB", (CARD_W, total_h), BG)
    draw = ImageDraw.Draw(img)
    cx = CARD_W // 2
    y = 28 * S

    # Score
    if is_override:
        r = 24 * S
        ey = y + r
        draw.ellipse([cx - r, ey - r, cx + r, ey + r], fill=(245, 240, 235))
        draw.text((cx, ey), "✓", fill=MUTED, font=_font(24 * S), anchor="mm")
        y = ey + r + 8 * S
    else:
        st = str(result.get("total_score", 0))
        draw.text((cx, y), st, fill=color, font=score_f, anchor="mt")
        bb = draw.textbbox((cx, y), st, font=score_f, anchor="mt")
        draw.text((bb[2] + 4 * S, bb[3] - 14 * S), "/ 100", fill=MUTED, font=unit_f, anchor="lt")
        y = bb[3] + 6 * S

    # Job name
    jn = result.get("job_name_zh" if zh else "job_name_en", "")
    draw.text((cx, y), jn, fill=MUTED, font=job_f, anchor="mt")
    jbb = draw.textbbox((cx, y), jn, font=job_f, anchor="mt")
    y = jbb[3] + 4 * S

    # Risk label
    rl = result.get("risk_label_zh" if zh else "risk_label_en", "")
    draw.text((cx, y), rl, fill=(MUTED if is_override else color), font=label_f, anchor="mt")
    rbb = draw.textbbox((cx, y), rl, font=label_f, anchor="mt")
    y = rbb[3] + 14 * S

    # Advice card
    ct = y
    cb = ct + advice_h
    draw.rounded_rectangle([PAD, ct, CARD_W - PAD, cb], radius=12 * S, fill=WHITE, outline=BORDER)
    at = "分析与建议" if zh else "Analysis & Advice"
    draw.text((PAD + INNER, ct + INNER), at, fill=INK, font=title_f)
    ty = ct + INNER + 20 * S
    for line in advice_lines:
        if line:
            draw.text((PAD + INNER, ty), line, fill=INK2, font=body_f)
        ty += line_h
    y = cb + 10 * S

    # Dimension breakdown
    if breakdown:
        labels_zh = ["职业类型", "产出形式", "知识类型", "委托能力", "容错率", "职级定位"]
        labels_en = ["Job Type", "Output Form", "Knowledge", "Delegation", "Tolerance", "Career Level"]
        labels = labels_zh if zh else labels_en
        dt = y
        db = dt + dim_h
        draw.rounded_rectangle([PAD, dt, CARD_W - PAD, db], radius=12 * S, fill=WHITE, outline=BORDER)
        draw.text((PAD + INNER, dt + INNER), "维度拆解" if zh else "Breakdown", fill=INK, font=title_f)
        ry = dt + INNER + 24 * S
        for i, sc in enumerate(breakdown):
            if i >= len(labels):
                break
            draw.text((PAD + INNER, ry + 3 * S), labels[i], fill=MUTED, font=dim_label_f)
            # Tag pill
            tt = _tag_text(sc, zh)
            ts = _tag_style(sc)
            tw = int(draw.textlength(tt, font=tag_f)) + 16 * S
            th = 18 * S
            tx = CARD_W - PAD - INNER - tw
            draw.rounded_rectangle([tx, ry, tx + tw, ry + th], radius=9 * S, fill=ts["bg"], outline=ts["bd"])
            draw.text((tx + tw // 2, ry + th // 2), tt, fill=ts["t"], font=tag_f, anchor="mm")
            ry += 24 * S
        y = db + 10 * S

    # Footer
    ft = "willaitakemyjobs.com" if zh else "willaitakemyjobs.com"
    draw.text((cx, total_h - 28 * S), ft, fill=FOOTER_C, font=footer_f, anchor="mb")

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
