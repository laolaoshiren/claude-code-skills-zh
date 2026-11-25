#!/usr/bin/env python3
"""
generate_social_preview.py — 生成仓库与官网统一社交预览图 (docs/social-preview.png)

特性：
1. 标准 1280x640 (2:1) 尺寸，内部采用 2x 超采样抗锯齿渲染，边缘与文字锐利清晰
2. 自动从 README.md 与 skills/ 目录读取最新统计口径（亦支持命令行参数覆盖）
3. 优先使用 Windows 微软雅黑 (msyhbd.ttc / msyh.ttc) 与 Consolas，并提供 macOS / Linux 跨平台字体回退
4. 确定性输出（固定无时间戳 PNG 元数据），体积严格控制在 500KB 以内

用法：
    python scripts/generate_social_preview.py
    python scripts/generate_social_preview.py --output docs/social-preview.png
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo


def _configure_stdio() -> None:
    """避免 Windows GBK/CP936 终端输出中文时触发编码异常。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")


_configure_stdio()

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "social-preview.png"
README_PATH = REPO_ROOT / "README.md"
SKILLS_DIR = REPO_ROOT / "skills"

CANVAS_W = 1280
CANVAS_H = 640
SCALE = 2
MAX_BYTES = 500 * 1024


# ── 跨平台字体解析 ────────────────────────────────────────────────────────────

BOLD_CJK_CANDIDATES: Sequence[str] = (
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/source-han-sans/SourceHanSansSC-Bold.otf",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
)

REGULAR_CJK_CANDIDATES: Sequence[str] = (
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simsun.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
)

BOLD_MONO_CANDIDATES: Sequence[str] = (
    r"C:\Windows\Fonts\consolab.ttf",
    r"C:\Windows\Fonts\CascadiaMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    *BOLD_CJK_CANDIDATES,
)


def load_font(
    candidates: Iterable[str],
    size_px: float,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    scaled_size = int(round(size_px * SCALE))
    for raw_path in candidates:
        path = Path(raw_path)
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), scaled_size)
            except OSError:
                continue
    raise RuntimeError(
        "未找到可用的中文字体，请确认系统已安装 Microsoft YaHei / PingFang / Noto Sans CJK。"
    )


# ── 仓库统计读取 ──────────────────────────────────────────────────────────────

def _classify_category_header(line: str) -> str | None:
    """与 scripts/sync_readme_to_site.py 保持一致的 8 大分类标题识别逻辑。"""
    stripped = line.strip()
    if not stripped.startswith("### "):
        return None
    if "🏆" in stripped and ("万星" in stripped or "热门与高潜" in stripped):
        return "star"
    if "平台运营" in stripped or "自媒体" in stripped:
        return "platform"
    if "💻" in stripped and "开发效率" in stripped:
        return "dev"
    if "🎨" in stripped and "内容创作" in stripped:
        return "creative"
    if "🔬" in stripped and "学术科研" in stripped:
        return "academic"
    if "🤖" in stripped and "Agent" in stripped:
        return "agent"
    if "💰" in stripped and ("金融" in stripped or "商业" in stripped):
        return "finance"
    if "🌏" in stripped and "中文专属" in stripped:
        return "chinese"
    return None


def detect_repo_metrics() -> tuple[str, int, int]:
    """从 README.md 和 skills/ 读取当前精选数口径、原创技能数与分类数。"""
    curated_display = "452+"
    original_count = 22
    category_count = 8

    if README_PATH.is_file():
        readme_text = README_PATH.read_text(encoding="utf-8")
        badge_match = re.search(r"skills-(\d+)%2B", readme_text)
        if badge_match:
            curated_display = f"{badge_match.group(1)}+"
        else:
            quote_match = re.search(r"精选\s*(\d+\+)", readme_text)
            if quote_match:
                curated_display = quote_match.group(1)

        found_cats = {
            cat
            for raw_line in readme_text.splitlines()
            if (cat := _classify_category_header(raw_line)) is not None
        }
        if found_cats:
            category_count = len(found_cats)

    if SKILLS_DIR.is_dir():
        skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
        if skill_files:
            original_count = len(skill_files)

    return curated_display, original_count, category_count


# ── 几何与排版辅助函数 ────────────────────────────────────────────────────────

def s(val: float) -> int:
    return int(round(val * SCALE))


def text_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> tuple[float, float]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return (bbox[2] - bbox[0]) / SCALE, (bbox[3] - bbox[1]) / SCALE


def draw_text_vc(
    draw: ImageDraw.ImageDraw,
    x: float,
    cy: float,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, ...],
) -> float:
    """在逻辑坐标 x 处绘制文本，使其视觉边界框垂直居中于 cy，返回绘制后的右边界逻辑 x。"""
    bbox = draw.textbbox((0, 0), text, font=font)
    px = s(x) - bbox[0]
    py = s(cy) - (bbox[1] + bbox[3]) / 2.0
    draw.text((px, py), text, font=font, fill=fill)
    return x + (bbox[2] - bbox[0]) / SCALE


def draw_text_center(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, ...],
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    px = s(cx) - (bbox[0] + bbox[2]) / 2.0
    py = s(cy) - (bbox[1] + bbox[3]) / 2.0
    draw.text((px, py), text, font=font, fill=fill)


def draw_diamond(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    fill: tuple[int, ...],
) -> None:
    pts = [
        (s(cx), s(cy - radius)),
        (s(cx + radius), s(cy)),
        (s(cx), s(cy + radius)),
        (s(cx - radius), s(cy)),
    ]
    draw.polygon(pts, fill=fill)


def draw_sparkle(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    outer_r: float,
    inner_r: float,
    fill: tuple[int, ...],
) -> None:
    pts = [
        (s(cx), s(cy - outer_r)),
        (s(cx + inner_r), s(cy - inner_r)),
        (s(cx + outer_r), s(cy)),
        (s(cx + inner_r), s(cy + inner_r)),
        (s(cx), s(cy + outer_r)),
        (s(cx - inner_r), s(cy + inner_r)),
        (s(cx - outer_r), s(cy)),
        (s(cx - inner_r), s(cy - inner_r)),
    ]
    draw.polygon(pts, fill=fill)


def draw_prompt_chevron(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    fill: tuple[int, ...],
) -> None:
    """绘制清晰的终端 `>_` 矢量图标，避免字体差异。"""
    lw = s(2.2)
    draw.line(
        [(s(cx - 6), s(cy - 5)), (s(cx - 1), s(cy)), (s(cx - 6), s(cy + 5))],
        fill=fill,
        width=lw,
        joint="curve",
    )
    draw.line(
        [(s(cx + 1), s(cy + 5)), (s(cx + 7), s(cy + 5))],
        fill=fill,
        width=lw,
    )


# ── 主画布渲染 ────────────────────────────────────────────────────────────────

def render_social_preview(
    curated_display: str,
    original_count: int,
    category_count: int,
) -> Image.Image:
    w2, h2 = CANVAS_W * SCALE, CANVAS_H * SCALE
    base = Image.new("RGBA", (w2, h2), (17, 20, 36, 255))

    # 1. 背景几何光晕层（延续原图深蓝底 + 右上靛紫圆 + 左下青绿圆品牌语言）
    bg_layer = Image.new("RGBA", (w2, h2), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_layer)

    # 右上靛紫几何大圆与柔和外环
    bg_draw.ellipse(
        (s(760), s(-270), s(1480), s(450)),
        fill=(43, 39, 94, 175),
        outline=(108, 92, 231, 58),
        width=s(1.5),
    )
    bg_draw.ellipse(
        (s(850), s(-190), s(1400), s(360)),
        fill=(56, 48, 118, 90),
    )

    # 左下青绿几何大圆与柔和外环
    bg_draw.ellipse(
        (s(-180), s(280), s(520), s(980)),
        fill=(18, 69, 88, 180),
        outline=(0, 229, 204, 52),
        width=s(1.5),
    )
    bg_draw.ellipse(
        (s(-90), s(360), s(430), s(880)),
        fill=(16, 92, 108, 85),
    )

    # 科技感细微点阵（仅分布在右上背景区域，干净克制）
    for gx in range(650, 1225, 28):
        for gy in range(44, 290, 28):
            bg_draw.ellipse(
                (s(gx - 1.2), s(gy - 1.2), s(gx + 1.2), s(gy + 1.2)),
                fill=(162, 155, 254, 34),
            )

    # 顶部细微高光条（安全边距内）
    base = Image.alpha_composite(base, bg_layer)

    # 2. 字体加载
    f_title = load_font(BOLD_CJK_CANDIDATES, 56)
    f_subtitle = load_font(REGULAR_CJK_CANDIDATES, 20.5)
    f_brand_mark = load_font(BOLD_CJK_CANDIDATES, 22)
    f_header_mono = load_font(BOLD_MONO_CANDIDATES, 18.5)
    f_header_tag = load_font(BOLD_CJK_CANDIDATES, 16.5)

    f_term_title = load_font(BOLD_CJK_CANDIDATES, 15)
    f_term_code = load_font(BOLD_MONO_CANDIDATES, 15.5)
    f_term_hint = load_font(REGULAR_CJK_CANDIDATES, 14.5)

    f_metric_num = load_font(BOLD_CJK_CANDIDATES, 44)
    f_metric_unit = load_font(BOLD_CJK_CANDIDATES, 24)
    f_metric_badge = load_font(BOLD_CJK_CANDIDATES, 13.5)
    f_metric_label = load_font(BOLD_CJK_CANDIDATES, 22)
    f_metric_sub = load_font(REGULAR_CJK_CANDIDATES, 15.5)

    f_pill = load_font(BOLD_CJK_CANDIDATES, 19.5)

    ui = Image.new("RGBA", (w2, h2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ui)

    left_x = 72
    right_x = 1208
    content_w = right_x - left_x  # 1136

    # ── Row 1: 顶部品牌标识 + 仓库路径 + 开源标识 (y = 48..88) ───────────────
    top_y1, top_y2 = 48, 88
    top_cy = (top_y1 + top_y2) / 2.0

    # 迷你「中」品牌图标（呼应 .claude-plugin/icon.png）
    draw.rounded_rectangle(
        (s(left_x), s(top_y1), s(left_x + 40), s(top_y2)),
        radius=s(10),
        fill=(26, 30, 56, 240),
        outline=(108, 92, 231, 180),
        width=s(1.5),
    )
    draw_text_center(draw, left_x + 20, top_cy - 1, "中", f_brand_mark, (248, 250, 252, 255))

    # 仓库标识胶囊 laolaoshiren/claude-code-skills-zh
    repo_slug = "laolaoshiren/claude-code-skills-zh"
    slug_w, _ = text_size(draw, repo_slug, f_header_mono)
    repo_pill_x1 = left_x + 50
    repo_pill_x2 = repo_pill_x1 + 36 + slug_w + 18
    draw.rounded_rectangle(
        (s(repo_pill_x1), s(top_y1), s(repo_pill_x2), s(top_y2)),
        radius=s(20),
        fill=(24, 29, 52, 220),
        outline=(162, 155, 254, 95),
        width=s(1.2),
    )
    draw.ellipse(
        (s(repo_pill_x1 + 15), s(top_cy - 4.5), s(repo_pill_x1 + 24), s(top_cy + 4.5)),
        fill=(0, 229, 204, 255),
    )
    draw_text_vc(draw, repo_pill_x1 + 32, top_cy, repo_slug, f_header_mono, (226, 232, 240, 255))

    # 右上角辅助徽章
    right_badge_text = "开源免费 · 人工核验 · 持续更新"
    rb_w, _ = text_size(draw, right_badge_text, f_header_tag)
    rb_x2 = right_x
    rb_x1 = rb_x2 - (rb_w + 38)
    draw.rounded_rectangle(
        (s(rb_x1), s(top_y1), s(rb_x2), s(top_y2)),
        radius=s(20),
        fill=(24, 29, 52, 205),
        outline=(108, 92, 231, 95),
        width=s(1.2),
    )
    draw_sparkle(draw, rb_x1 + 17, top_cy, 5.5, 2.0, (162, 155, 254, 255))
    draw_text_vc(draw, rb_x1 + 28, top_cy, right_badge_text, f_header_tag, (199, 210, 254, 255))

    # ── Row 2: 主标题区（左）+ 终端一键安装卡片（右）(y = 108..276) ──────────
    draw_text_vc(draw, left_x, 140, "Claude Code Skills", f_title, (255, 255, 255, 255))
    draw_text_vc(draw, left_x, 210, "中文精选集", f_title, (0, 229, 204, 255))
    draw_text_vc(
        draw,
        left_x,
        263,
        "面向中文开发者的 Skills / Agents / Plugins 精选资源库",
        f_subtitle,
        (165, 177, 198, 255),
    )

    # 右侧深色毛玻璃终端卡片 (x = 668..1208, y = 110..274)
    term_x1, term_y1, term_x2, term_y2 = 668, 110, right_x, 274
    draw.rounded_rectangle(
        (s(term_x1), s(term_y1), s(term_x2), s(term_y2)),
        radius=s(16),
        fill=(14, 17, 31, 236),
        outline=(108, 92, 231, 130),
        width=s(1.5),
    )
    # 终端顶栏分隔线
    header_bottom = term_y1 + 34
    draw.line(
        [(s(term_x1 + 1), s(header_bottom)), (s(term_x2 - 1), s(header_bottom))],
        fill=(162, 155, 254, 42),
        width=s(1),
    )
    # 窗口圆点
    dot_cy = term_y1 + 17
    for idx, color in enumerate(((255, 95, 86, 235), (255, 189, 46, 235), (39, 201, 63, 235))):
        cx = term_x1 + 20 + idx * 15
        draw.ellipse((s(cx - 4.5), s(dot_cy - 4.5), s(cx + 4.5), s(dot_cy + 4.5)), fill=color)

    draw_text_vc(
        draw,
        term_x1 + 72,
        dot_cy,
        "Claude Code · 复制即装",
        f_term_title,
        (165, 180, 252, 255),
    )

    # 终端真实命令展示
    tx = term_x1 + 20
    c1_end = draw_text_vc(draw, tx, term_y1 + 60, "> ", f_term_code, (0, 229, 204, 255))
    c1_end = draw_text_vc(draw, c1_end, term_y1 + 60, "/plugin ", f_term_code, (162, 155, 254, 255))
    draw_text_vc(draw, c1_end, term_y1 + 60, "marketplace add \\", f_term_code, (241, 245, 249, 255))

    draw_text_vc(
        draw,
        tx + 24,
        term_y1 + 88,
        "laolaoshiren/claude-code-skills-zh",
        f_term_code,
        (116, 185, 255, 255),
    )

    c3_end = draw_text_vc(draw, tx, term_y1 + 118, "> ", f_term_code, (0, 229, 204, 255))
    c3_end = draw_text_vc(draw, c3_end, term_y1 + 118, "/plugin ", f_term_code, (162, 155, 254, 255))
    c3_end = draw_text_vc(draw, c3_end, term_y1 + 118, "install ", f_term_code, (241, 245, 249, 255))
    draw_text_vc(draw, c3_end, term_y1 + 118, "zh-skills@claude-code-skills-zh", f_term_code, (0, 229, 204, 255))

    draw_text_vc(
        draw,
        tx,
        term_y1 + 145,
        "# 一条命令装齐原创中文技能，亦支持单技能按需复制",
        f_term_hint,
        (124, 138, 166, 255),
    )

    # ── Row 3: 三大核心指标卡片 (y = 300..432) ───────────────────────────────
    card_y1, card_y2 = 300, 432
    card_gap = 28
    card_w = (content_w - card_gap * 2) / 3.0  # 360.0

    metrics = [
        {
            "num": curated_display,
            "unit": "",
            "label": "精选技能",
            "sub": "人工核验可复用资产",
            "badge": "中文说明",
            "accent": (0, 229, 204, 255),
            "border": (0, 229, 204, 115),
            "bg": (19, 39, 56, 222),
            "badge_bg": (0, 229, 204, 34),
        },
        {
            "num": str(original_count),
            "unit": " 个",
            "label": "原创中文技能",
            "sub": "本土研发与内容工作流",
            "badge": "开箱即用",
            "accent": (162, 155, 254, 255),
            "border": (162, 155, 254, 120),
            "bg": (28, 29, 58, 222),
            "badge_bg": (162, 155, 254, 36),
        },
        {
            "num": str(category_count),
            "unit": " 大",
            "label": "场景分类",
            "sub": "研发 · 创作 · 科研 · 国内",
            "badge": "精准检索",
            "accent": (116, 185, 255, 255),
            "border": (116, 185, 255, 120),
            "bg": (22, 33, 60, 222),
            "badge_bg": (116, 185, 255, 36),
        },
    ]

    for i, m in enumerate(metrics):
        cx1 = left_x + i * (card_w + card_gap)
        cx2 = cx1 + card_w
        draw.rounded_rectangle(
            (s(cx1), s(card_y1), s(cx2), s(card_y2)),
            radius=s(18),
            fill=m["bg"],
            outline=m["border"],
            width=s(1.5),
        )
        # 左侧竖向高亮指示条
        draw.rounded_rectangle(
            (s(cx1 + 16), s(card_y1 + 22), s(cx1 + 21), s(card_y2 - 22)),
            radius=s(2.5),
            fill=m["accent"],
        )

        # 数字 + 单位
        num_right = draw_text_vc(
            draw,
            cx1 + 34,
            card_y1 + 46,
            m["num"],
            f_metric_num,
            (255, 255, 255, 255),
        )
        if m["unit"]:
            draw_text_vc(
                draw,
                num_right + 2,
                card_y1 + 51,
                m["unit"],
                f_metric_unit,
                m["accent"],
            )

        # 右上小标签
        bw, _ = text_size(draw, m["badge"], f_metric_badge)
        bx2 = cx2 - 18
        bx1 = bx2 - (bw + 20)
        by1, by2 = card_y1 + 20, card_y1 + 46
        draw.rounded_rectangle(
            (s(bx1), s(by1), s(bx2), s(by2)),
            radius=s(13),
            fill=m["badge_bg"],
            outline=(*m["accent"][:3], 95),
            width=s(1),
        )
        draw_text_center(draw, (bx1 + bx2) / 2.0, (by1 + by2) / 2.0, m["badge"], f_metric_badge, m["accent"])

        # 指标主名称 + 副说明（严格校验右侧留白 >= 16px）
        lbl_right = draw_text_vc(
            draw,
            cx1 + 34,
            card_y1 + 98,
            m["label"],
            f_metric_label,
            (241, 245, 249, 255),
        )
        sub_right = draw_text_vc(
            draw,
            lbl_right + 10,
            card_y1 + 99,
            m["sub"],
            f_metric_sub,
            (154, 168, 192, 255),
        )
        if sub_right > cx2 - 16:
            raise RuntimeError(f"指标卡片副标题超出安全内边距: {m['label']} {m['sub']} ({sub_right:.1f} > {cx2 - 16:.1f})")

    # ── Row 4: 四大核心卖点标签组（双行 Bento 对齐 y = 456..574） ─────────────
    def draw_bento_pills_row(
        y1: float,
        y2: float,
        items: list[dict],
        gap: float = 20.0,
    ) -> None:
        cy = (y1 + y2) / 2.0
        # 按文本自然宽度加相同富余空间，精确铺满 left_x..right_x
        natural_widths: list[float] = []
        for item in items:
            tw, _ = text_size(draw, item["text"], f_pill)
            natural_widths.append(tw + 52.0)

        total_natural = sum(natural_widths)
        total_gaps = gap * (len(items) - 1)
        extra_each = (content_w - total_gaps - total_natural) / len(items)
        if extra_each < -12:
            raise RuntimeError(f"标签行宽度超出安全边界: { [it['text'] for it in items] }")

        cur_x = float(left_x)
        for idx, item in enumerate(items):
            pw = natural_widths[idx] + extra_each
            px1 = cur_x
            px2 = right_x if idx == len(items) - 1 else (cur_x + pw)

            draw.rounded_rectangle(
                (s(px1), s(y1), s(px2), s(y2)),
                radius=s(14),
                fill=item["bg"],
                outline=item["border"],
                width=s(1.3),
            )

            # 内部内容整体水平居中，视觉更均衡
            tw, _ = text_size(draw, item["text"], f_pill)
            group_w = 22.0 + tw
            gx = (px1 + px2 - group_w) / 2.0
            icon_cx = gx + 7.0

            kind = item["icon"]
            accent = item["accent"]
            if kind == "dot":
                draw.ellipse(
                    (s(icon_cx - 5), s(cy - 5), s(icon_cx + 5), s(cy + 5)),
                    fill=accent,
                )
            elif kind == "prompt":
                draw_prompt_chevron(draw, icon_cx, cy, accent)
            elif kind == "diamond":
                draw_diamond(draw, icon_cx, cy, 5.8, accent)
            elif kind == "sparkle":
                draw_sparkle(draw, icon_cx, cy, 6.5, 2.4, accent)

            draw_text_vc(draw, gx + 22.0, cy, item["text"], f_pill, item["text_color"])
            cur_x = px2 + gap

    draw_bento_pills_row(
        456,
        506,
        [
            {
                "icon": "dot",
                "text": "公众号 / 小红书 / 飞书 / 企微国内生态",
                "accent": (0, 229, 204, 255),
                "border": (0, 229, 204, 105),
                "bg": (18, 36, 52, 215),
                "text_color": (241, 245, 249, 255),
            },
            {
                "icon": "dot",
                "text": "兼容 Claude Code / Codex / Cursor / Gemini CLI",
                "accent": (162, 155, 254, 255),
                "border": (162, 155, 254, 110),
                "bg": (26, 28, 54, 215),
                "text_color": (241, 245, 249, 255),
            },
        ],
        gap=22.0,
    )

    draw_bento_pills_row(
        522,
        572,
        [
            {
                "icon": "prompt",
                "text": "/plugin 一键安装",
                "accent": (0, 229, 204, 255),
                "border": (0, 229, 204, 105),
                "bg": (18, 38, 48, 220),
                "text_color": (241, 245, 249, 255),
            },
            {
                "icon": "diamond",
                "text": "claude-skills.bt199.com",
                "accent": (116, 185, 255, 255),
                "border": (116, 185, 255, 115),
                "bg": (20, 32, 58, 220),
                "text_color": (186, 230, 253, 255),
            },
            {
                "icon": "sparkle",
                "text": "跨类实时搜索 · 按场景复制即装",
                "accent": (162, 155, 254, 255),
                "border": (108, 92, 231, 105),
                "bg": (25, 27, 50, 215),
                "text_color": (226, 232, 240, 255),
            },
        ],
        gap=20.0,
    )

    composed = Image.alpha_composite(base, ui).convert("RGB")
    final_img = composed.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    return final_img


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 docs/social-preview.png 社交预览图")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="输出 PNG 文件路径（默认 docs/social-preview.png）",
    )
    parser.add_argument("--curated", type=str, default=None, help="精选技能展示口径，如 452+")
    parser.add_argument("--original", type=int, default=None, help="原创中文技能数量，如 22")
    parser.add_argument("--categories", type=int, default=None, help="大场景分类数量，如 8")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    auto_curated, auto_original, auto_categories = detect_repo_metrics()
    curated = args.curated or auto_curated
    original = args.original if args.original is not None else auto_original
    categories = args.categories if args.categories is not None else auto_categories

    img = render_social_preview(curated, original, categories)
    output_path: Path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pnginfo = PngInfo()
    img.save(output_path, format="PNG", optimize=True, pnginfo=pnginfo)

    size_bytes = output_path.stat().st_size
    if size_bytes > MAX_BYTES:
        # 若超采样平滑色彩导致体积偏大，使用高质量 256 色自适应量化兜底
        quantized = img.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        quantized.save(output_path, format="PNG", optimize=True, pnginfo=pnginfo)
        size_bytes = output_path.stat().st_size

    if size_bytes > MAX_BYTES:
        raise RuntimeError(f"生成的预览图体积 {size_bytes} bytes 超过 500KB 上限")

    print(
        f"已生成 {output_path} ({CANVAS_W}x{CANVAS_H}, {size_bytes / 1024:.1f} KB) | "
        f"口径: {curated} 精选技能 · {original} 个原创中文技能 · {categories} 大场景分类"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
