#!/usr/bin/env python3
"""
build_pptx.py — Group 14 · INS3044 Final Presentation
Task and Project Management System

Cartesian design (warm-neutral palette, Playfair/Georgia serifs, restrained).
16:9 widescreen. Clean API mirroring the proven reference script.

Run: python3 docs/slides/build_pptx.py
Output: docs/slides/Group14_INS3044_Cartesian.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

# ── Cartesian palette ──────────────────────────────────────────────────────
INK        = RGBColor(0x2B, 0x24, 0x19)   # deep walnut
INK_SOFT   = RGBColor(0x5C, 0x4F, 0x3F)   # muted brown
MUTED      = RGBColor(0x8A, 0x7A, 0x66)   # warm grey
PARCHMENT  = RGBColor(0xF5, 0xEF, 0xE6)   # warm off-white
PARCH_ELEV = RGBColor(0xED, 0xE4, 0xD3)   # card fill
PARCH_SURF = RGBColor(0xFB, 0xF8, 0xF2)   # highlight
RULE       = RGBColor(0xD9, 0xCD, 0xB8)   # hairline
ACCENT     = RGBColor(0x8C, 0x5A, 0x2E)   # burnt sienna
ACC_SOFT   = RGBColor(0xC4, 0x9A, 0x6C)   # light tan
ACC_BG     = RGBColor(0xE8, 0xD5, 0xBC)   # soft tan bg
OK         = RGBColor(0x5B, 0x6B, 0x47)   # olive
WARN       = RGBColor(0xA6, 0x5D, 0x3F)   # rust
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)

# ── Fonts ──────────────────────────────────────────────────────────────────────
SERIF = "Playfair Display"    # PowerPoint falls back to Georgia
SANS  = "Inter"              # PowerPoint falls back to Calibri
MONO  = "JetBrains Mono"     # PowerPoint falls back to Consolas

# ── Geometry: 16:9 widescreen ────────────────────────────────────────────────
SW = Inches(13.333)
SH = Inches(7.5)
MG = Inches(0.7)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers — mirror the proven reference API exactly
# ─────────────────────────────────────────────────────────────────────────────

def _I(v):
    """Coerce any EMU-like value to a plain int. PowerPoint rejects float EMUs."""
    if v is None:
        return 0
    if isinstance(v, int):
        return v
    # pptx.util.Length subclasses int, but arithmetic may yield float
    if isinstance(v, float):
        return int(v)
    # Length, Emu, Inches — all subclass int but division can yield float
    return int(v)


def set_bg(slide, color):
    """Solid background fill on a slide."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=None):
    """Add a rectangle shape. All dims in EMU (use Inches())."""
    x, y, w, h = _I(x), _I(y), _I(w), _I(h)
    if w <= 0 or h <= 0:
        return None
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(int(line_w) if line_w else 0.75)
    return shp


def add_hline(slide, x, y, w, color, weight=Pt(0.75)):
    """Horizontal hairline."""
    x, y, w = _I(x), _I(y), _I(w)
    shp = slide.shapes.add_connector(1, x, y, x + w, y)
    shp.line.color.rgb = color
    shp.line.width = weight
    return shp


def add_vline(slide, x, y, h, color, weight=Pt(0.75)):
    """Vertical hairline."""
    x, y, h = _I(x), _I(y), _I(h)
    shp = slide.shapes.add_connector(1, x, y, x, y + h)
    shp.line.color.rgb = color
    shp.line.width = weight
    return shp


def add_text(slide, x, y, w, h, text, *,
             font=SANS, size=14, bold=False, italic=False,
             color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             line_spacing=1.0, letter_spacing=None):
    """Add a text box. All dims in EMU."""
    x, y, w, h = _I(x), _I(y), _I(w), _I(h)
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left   = Inches(0.06)
    tf.margin_right  = Inches(0.06)
    tf.margin_top    = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.word_wrap = True
    tf.vertical_anchor = anchor

    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        f = r.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = color
        if letter_spacing is not None:
            rPr = r._r.get_or_add_rPr()
            rPr.set("spc", str(int(letter_spacing)))
    return tb


def add_table(slide, data, x, y, w, h, *,
              col_widths=None, row_fills=None, font_size=10):
    """Add a styled table. data[0] = header row. All dims in EMU."""
    rows = len(data)
    cols = len(data[0])
    tbl_shape = slide.shapes.add_table(rows, cols, x, y, w, h)
    tbl = tbl_shape.table

    # Column widths
    if col_widths:
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = _I(cw)

    # Row heights — distribute evenly. PowerPoint rejects float EMUs.
    row_h = _I(h) // rows
    for r in tbl.rows:
        r.height = row_h

    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.margin_left   = Inches(0.08)
            cell.margin_right  = Inches(0.08)
            cell.margin_top    = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.text = ""
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = str(val)
            run.font.name  = SANS
            run.font.size  = Pt(font_size)
            run.font.bold  = (ri == 0)
            run.font.color.rgb = WHITE if ri == 0 else INK

            # Fill
            cell.fill.solid()
            if ri == 0:
                cell.fill.fore_color.rgb = ACCENT
            elif row_fills and ri - 1 < len(row_fills) and row_fills[ri - 1]:
                cell.fill.fore_color.rgb = row_fills[ri - 1]
            else:
                cell.fill.fore_color.rgb = PARCHMENT

    return tbl


def kpi_card(slide, x, y, w, h, label, value, sub="", accent=False):
    """KPI card: rounded-rect outline, big serif number, small label."""
    fill_c = ACC_SOFT if accent else PARCH_ELEV
    line_c = ACCENT   if accent else RULE
    add_rect(slide, x, y, w, h, fill=fill_c, line=line_c, line_w=0.75)
    # Value — big serif
    add_text(slide, x + Inches(0.08), y + Inches(0.08),
             w - Inches(0.16), h * 0.55,
             value, font=SERIF, size=24, bold=True,
             color=ACCENT if accent else INK, align=PP_ALIGN.CENTER)
    # Label
    add_text(slide, x + Inches(0.06), y + h * 0.52,
             w - Inches(0.12), h * 0.22,
             label, font=SANS, size=9, color=INK_SOFT, align=PP_ALIGN.CENTER)
    if sub:
        add_text(slide, x + Inches(0.06), y + h * 0.74,
                 w - Inches(0.12), h * 0.2,
                 sub, font=SANS, size=8, italic=True,
                 color=MUTED, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────────────────────────────────────
# Build presentation
# ─────────────────────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = SW
prs.slide_height = SH
blank = prs.slide_layouts[6]

TOTAL = 31  # fixed slide total (footer counter)
_slide_num = [0]

def nxt():
    _slide_num[0] += 1
    return _slide_num[0]


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
set_bg(s, PARCHMENT)

# Top hairline
add_hline(s, Inches(0), Inches(0.04), SW, RULE, Pt(1))

# Course kicker
add_text(s, Inches(0.9), Inches(0.6), Inches(11), Inches(0.4),
         "INS3044 · IT Project Management",
         font=SANS, size=13, color=MUTED)

# Main title — two lines
add_text(s, Inches(0.9), Inches(1.2), Inches(11.5), Inches(1.1),
         "Task & Project", font=SERIF, size=58, bold=True, color=INK)
add_text(s, Inches(0.9), Inches(2.1), Inches(11.5), Inches(0.9),
         "Management System", font=SERIF, size=58, bold=True, color=INK)

# Tagline
add_text(s, Inches(0.9), Inches(3.1), Inches(9), Inches(0.5),
         "An unhurried 14-week build",
         font=SERIF, size=20, italic=True, color=INK_SOFT)

# Hairline rule
add_hline(s, Inches(0.9), Inches(3.68), Inches(11.533), RULE, Pt(1))

# Member cards — 4 across
members = [
    ("PM · Leader",       "Nguyễn Long Đức",  "23070435"),
    ("Developer",         "Phạm Hồ Bảo",       "23070455"),
    ("UI / UX Designer",  "Kiều Bá Thịnh",      "23070247"),
    ("Quality Assurance", "Đỗ Huy Hiếu",        "23070325"),
]
card_w = Inches(2.7)
card_gap = Inches(0.2)
for i, (role, name, sid) in enumerate(members):
    cx = Inches(0.9) + i * (card_w + card_gap)
    add_rect(s, cx, Inches(3.85), card_w, Inches(1.1),
             fill=PARCH_ELEV, line=RULE, line_w=0.75)
    add_text(s, cx + Inches(0.1), Inches(3.9), Inches(2.5), Inches(0.28),
             role, font=SANS, size=9, color=MUTED)
    add_text(s, cx + Inches(0.1), Inches(4.15), Inches(2.5), Inches(0.32),
             name, font=SERIF, size=13, bold=True, color=INK)
    add_text(s, cx + Inches(0.1), Inches(4.52), Inches(2.5), Inches(0.28),
             sid, font=SANS, size=10, color=MUTED)

# Footer rule + meta
add_hline(s, Inches(0.9), Inches(6.62), Inches(11.533), RULE, Pt(0.75))
add_text(s, Inches(0.9), Inches(6.68), Inches(6), Inches(0.3),
         "Instructors: Dr Nguyễn Phương Anh · MS Đỗ Tiến Thành",
         font=SANS, size=10, color=MUTED)
add_text(s, Inches(0.9), Inches(6.92), Inches(6), Inches(0.3),
         "Faculty of Applied Sciences · VNU · June 2026",
         font=SANS, size=10, color=MUTED)

s.notes_slide.notes_text_frame.text = (
    "Welcome everyone. Group 14: Đức as PM, Bảo on development, "
    "Thịnh on UI/UX, Hiếu leading QA. We've spent 14 weeks building a "
    "web-based Task and Project Management System, applying every major "
    "discipline of IT project management. The tagline 'an unhurried 14-week "
    "build' captures our approach — sound process over speed. Eight sections: "
    "WBS, PERT, CPM, budgeting, risk, communication, EVM, and the prototype demo."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — AGENDA
# ═══════════════════════════════════════════════════════════════════════════
sn = nxt()
s = prs.slides.add_slide(blank)
set_bg(s, PARCHMENT)

add_text(s, Inches(0.7), Inches(0.45), Inches(8), Inches(0.3),
         "OVERVIEW", font=SANS, size=10, bold=True, color=MUTED,
         letter_spacing=200)
add_hline(s, Inches(0.7), Inches(0.8), Inches(0.55), ACCENT, Pt(1.5))
add_text(s, Inches(0.7), Inches(0.9), Inches(12), Inches(0.8),
         "Eight sections, one project",
         font=SERIF, size=36, bold=True, color=INK)

sections = [
    ("§ I",  "Scope & Objectives",       "CLO 1, 2"),
    ("§ II", "Work Breakdown Structure",   "CLO 2, 5"),
    ("§ III","Timeline & Milestones",       "CLO 2, 4, 5"),
    ("§ IV", "Resource Management",       "CLO 2, 8, 9"),
    ("§ V",  "Risk Management",          "CLO 3, 6"),
    ("§ VI", "Communication",             "CLO 4, 5, 8, 9, 12"),
    ("§ VII","Monitoring & EVM",            "CLO 7"),
    ("§ VIII","Prototype & Lessons",       "CLO 7, 8, 9"),
]
col_w = Inches(5.6)
for i, (num, title, clo) in enumerate(sections):
    col = i % 2
    row = i // 2
    cx = Inches(0.7) + col * (col_w + Inches(0.3))
    cy = Inches(2.05) + row * Inches(1.12)
    add_rect(s, cx, cy, col_w, Inches(0.98), fill=PARCH_ELEV, line=RULE, line_w=0.75)
    add_text(s, cx + Inches(0.12), cy + Inches(0.06), Inches(0.8), Inches(0.88),
             num, font=SERIF, size=24, italic=True, color=ACCENT)
    add_text(s, cx + Inches(0.9), cy + Inches(0.1), Inches(4.4), Inches(0.38),
             title, font=SERIF, size=15, bold=True, color=INK)
    add_text(s, cx + Inches(0.9), cy + Inches(0.52), Inches(4.4), Inches(0.28),
             clo, font=SANS, size=10, color=MUTED)

add_hline(s, Inches(0.7), Inches(7.22), Inches(11.933), RULE, Pt(0.75))
add_text(s, Inches(0.7), Inches(7.27), Inches(5), Inches(0.28),
         "Group 14 · INS3044 · June 2026", font=SANS, size=9, color=MUTED)
add_text(s, Inches(12.3), Inches(7.27), Inches(1), Inches(0.28),
         f"{sn:02d} / {TOTAL:02d}",
         font=MONO, size=9, color=MUTED, align=PP_ALIGN.RIGHT)
s.notes_slide.notes_text_frame.text = (
    "Our presentation mirrors the full project management cycle across eight sections. "
    "We'll open with scope, move through WBS, schedule, budget, risk, and communication, "
    "then finish with EVM monitoring and the live prototype demo. Each section maps to "
    "specific CLOs in the INS3044 syllabus."
)


# ═══════════════════════════════════════════════════════════════════════════
# Section divider helper
# ═══════════════════════════════════════════════════════════════════════════
def section_divider(roman, title, cline=""):
    sn = nxt()
    s = prs.slides.add_slide(blank)
    set_bg(s, PARCHMENT)
    # Top + bottom hairlines
    add_hline(s, Inches(0), Inches(0.04), SW, RULE, Pt(1))
    add_hline(s, Inches(0), SH - Inches(0.04), SW, RULE, Pt(1))
    # § mark
    add_text(s, Inches(0.8), Inches(1.5), Inches(2.2), Inches(1.5),
             "§", font=SERIF, size=120, italic=True, color=ACCENT)
    # Roman numeral
    add_text(s, Inches(2.8), Inches(1.72), Inches(2), Inches(1),
             roman, font=SERIF, size=44, italic=True, color=ACC_SOFT)
    # Title
    add_text(s, Inches(0.8), Inches(3.4), Inches(11), Inches(1),
             title, font=SERIF, size=40, bold=True, color=INK)
    if cline:
        add_text(s, Inches(0.8), Inches(4.5), Inches(10), Inches(0.5),
                 cline, font=SANS, size=13, italic=True, color=MUTED)
    add_hline(s, Inches(0.8), SH - Inches(0.55), Inches(11.733), RULE, Pt(0.75))
    add_text(s, Inches(0.8), SH - Inches(0.5), Inches(5), Inches(0.28),
             "Group 14 · INS3044 · June 2026", font=SANS, size=9, color=MUTED)
    add_text(s, Inches(12.3), SH - Inches(0.5), Inches(1), Inches(0.28),
             f"{sn:02d} / {TOTAL:02d}",
             font=MONO, size=9, color=MUTED, align=PP_ALIGN.RIGHT)
    return s


# ═══════════════════════════════════════════════════════════════════════════
# Content slide helper
# ═══════════════════════════════════════════════════════════════════════════
def content_slide(eyebrow, title, notes="", accent_title=False):
    sn = nxt()
    s = prs.slides.add_slide(blank)
    set_bg(s, PARCHMENT)
    add_hline(s, Inches(0), Inches(0.04), SW, RULE, Pt(0.75))
    if eyebrow:
        add_text(s, Inches(0.7), Inches(0.14), Inches(8), Inches(0.32),
                 eyebrow.upper(), font=SANS, size=9, color=MUTED)
    add_text(s, Inches(0.7), Inches(0.44), Inches(12), Inches(0.78),
             title, font=SERIF, size=28, bold=True,
             color=ACCENT if accent_title else INK)
    add_hline(s, Inches(0.7), Inches(7.22), Inches(11.933), RULE, Pt(0.75))
    add_text(s, Inches(0.7), Inches(7.27), Inches(5), Inches(0.28),
             "Group 14 · INS3044 · June 2026", font=SANS, size=9, color=MUTED)
    add_text(s, Inches(12.3), Inches(7.27), Inches(1), Inches(0.28),
             f"{sn:02d} / {TOTAL:02d}",
             font=MONO, size=9, color=MUTED, align=PP_ALIGN.RIGHT)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — § I DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("I", "Scope & Objectives", "CLO 1, 2 · Ch. 1, 2, 3")
s.notes_slide.notes_text_frame.text = (
    "Section I sets the foundation — business context, in-scope and out-of-scope "
    "boundaries, and our five SMART objectives tied directly to the INS3044 CLOs."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — PROJECT KPIs
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Scope & Objectives", "Project at a Glance",
    notes=(
        "Four headline KPIs. BAC is 33.6 million VND from bottom-up estimation. "
        "Critical path is 43 working days — we'll derive that in Section III. "
        "Risk EMV of 3.08 million is covered by contingency plus management reserve. "
        "Five prototype features delivered live."
    )
)
kpis = [
    ("33,600,000 VND",  "Budget at Completion (BAC)",           "",         True),
    ("43 working days", "Critical Path Duration",                 "A→B→E→G→H",  False),
    ("3,080,000 VND",   "Total Risk EMV (Cost)",                 "6 risks",       False),
    ("5 core features",  "Prototype Feature Areas",                "≥ 3 req.",     False),
]
for i, (val, lbl, sub, acc) in enumerate(kpis):
    cx = Inches(0.7) + i * Inches(3.08)
    kpi_card(s, cx, Inches(1.55), Inches(2.9), Inches(1.8), lbl, val, sub, acc)

add_text(s, Inches(0.7), Inches(3.58), Inches(12), Inches(0.28),
         "BAC: Labour 24M · OH 20% · G&A reallocated · Contingency 2.4M · Mgmt reserve 0.68M",
         font=SANS, size=10, italic=True, color=MUTED)
add_text(s, Inches(0.7), Inches(3.95), Inches(12), Inches(0.28),
         "Risk EMV: Contingency 2,400,000 + Mgmt reserve 680,000 = 3,080,000 VND ✓",
         font=SANS, size=10, italic=True, color=MUTED)
add_hline(s, Inches(0.7), Inches(4.4), Inches(12), RULE, Pt(0.5))
add_text(s, Inches(0.7), Inches(4.5), Inches(12), Inches(0.4),
         "Team: Nguyễn Long Đức (23070435, PM) · Phạm Hồ Bảo (23070455, Dev) · "
         "Kiều Bá Thịnh (23070247, UI/UX) · Đỗ Huy Hiếu (23070325, QA)",
         font=SANS, size=11, color=INK_SOFT)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — IN-SCOPE / OUT-OF-SCOPE
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Scope & Objectives", "Scope Boundaries",
    notes=(
        "Left: explicit in-scope — agreed by all four members, traceable to registration. "
        "Right: deliberately excluded with rationale. Scope lock is our first defence "
        "against R2 scope creep."
    )
)
add_rect(s, Inches(0.7), Inches(1.55), Inches(5.8), Inches(0.4),
         fill=OK, line=None)
add_text(s, Inches(0.7), Inches(1.55), Inches(5.8), Inches(0.4),
         "IN SCOPE", font=SANS, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

in_scope = [
    "Project CRUD (create, read, update, delete)",
    "Task CRUD with user assignment",
    "Status workflow: To Do → In Progress → Done",
    "Task deadline with overdue highlighting",
    "Task progress % (0–100%) per task",
    "Project dashboard (counts & progress)",
    "Role-based UI: Admin / PM / Member",
    "Responsive single-page web application",
    "Functional prototype (≥ 3 features live)",
    "Full PM documentation (WBS, CPM, budget, risk, EVM)",
]
for i, item in enumerate(in_scope):
    add_text(s, Inches(0.75), Inches(2.0) + i * Inches(0.4), Inches(5.7), Inches(0.36),
             "·  " + item, font=SANS, size=9, color=INK)

add_rect(s, Inches(6.8), Inches(1.55), Inches(5.8), Inches(0.4),
         fill=WARN, line=None)
add_text(s, Inches(6.8), Inches(1.55), Inches(5.8), Inches(0.4),
         "OUT OF SCOPE", font=SANS, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
out_scope = [
    "Native iOS / Android application",
    "Real-time chat or messaging",
    "Billing, invoicing, payment processing",
    "Third-party integrations (Slack, GitHub, Outlook)",
    "Multi-tenancy (multiple organisations)",
    "Post-launch maintenance or support",
    "Automated email / push notifications",
]
for i, item in enumerate(out_scope):
    add_text(s, Inches(6.85), Inches(2.0) + i * Inches(0.4), Inches(5.7), Inches(0.36),
             "✗  " + item, font=SANS, size=9, color=INK)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — SMART OBJECTIVES
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Scope & Objectives", "SMART Objectives",
    notes=(
        "Five objectives, each Specific, Measurable, Achievable, Relevant, Time-bound. "
        "OBJ-1: prototype deliverables. OBJ-2: 480-hour budget. OBJ-3: quality at UAT. "
        "OBJ-4: risk EMV. OBJ-5: final submission. Every objective is tagged to a CLO."
    )
)
obj_data = [
    ["#",   "Objective",                                                                              "CLO"],
    ["OBJ-1","Deliver working prototype: task CRUD, assignment, deadline tracking, progress\n"
             "monitoring for 3 roles — demo at W10, submit at W14",                                   "CLO 1, 2"],
    ["OBJ-2","Complete all 16 WBS Level 3 packages within 480 person-hours (±10%)\n"
             "by Week 14; tracked weekly in Trello",                                                    "CLO 2, 4"],
    ["OBJ-3","Pass UAT with ≥ 80% test coverage and ≤ 10 defects/KLOC;\n"
             "UAT sign-off at Week 12",                                                                  "CLO 3, 6"],
    ["OBJ-4","Identify ≥ 6 risks; contingency reserve ≥ Total Risk EMV;\n"
             "risk register updated bi-weekly",                                                          "CLO 3, 6"],
    ["OBJ-5","Submit full ZIP package (report, prototype, PPTX+PDF, evidence)\n"
             "before Week 14 deadline",                                                                   "CLO 7, 8, 9"],
]
add_table(s, obj_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(4.0),
          col_widths=[Inches(0.72), Inches(10.58), Inches(1.0)],
          font_size=10)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — § II DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("II", "Work Breakdown Structure", "CLO 2, 5 · Ch. 4, 5")
s.notes_slide.notes_text_frame.text = (
    "Section II — the Work Breakdown Structure. Our definitive scope baseline: "
    "every deliverable maps to exactly one Level 3 work package. Three-level hierarchy, "
    "16 work packages, 480 person-hours total."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — WBS TREE
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Work Breakdown Structure", "WBS — Three-Level Hierarchy",
    notes=(
        "Level 1: the project itself. Level 2: seven branches. Level 3: 16 work packages. "
        "Total effort 480 person-hours — verified against the scope statement."
    )
)

wbs_items = [
    ("1.0",  "Task & Project Management System",  True,  True),
    ("1.1",  "Project Management",                  False, True),
    ("1.1.1","  Project Charter & Kickoff",        False, False),
    ("1.1.2","  Status Meetings (12 × 2 h)",      False, False),
    ("1.1.3","  Risk Reviews",                     False, False),
    ("1.1.4","  Final Report Writing",             False, False),
    ("1.2",  "Requirements & Analysis",             False, True),
    ("1.2.1","  Stakeholder Interviews",             False, False),
    ("1.2.2","  Requirements Document",             False, False),
    ("1.2.3","  Requirements Sign-off",             False, False),
    ("1.3",  "System Design",                       False, True),
    ("1.3.1","  UI/UX Design (Figma)",              False, False),
    ("1.3.2","  Database / Data-Model Schema",      False, False),
    ("1.3.3","  API / Service Contract",            False, False),
    ("1.4",  "Development",                         False, True),
    ("1.4.1","  Frontend (React + Vite + TS)",     False, False),
    ("1.4.2","  Backend / Persistence Layer",      False, False),
    ("1.4.3","  Integration & Wiring",              False, False),
    ("1.5",  "Testing & QA",                        False, True),
    ("1.5.1","  Unit Tests (Vitest)",               False, False),
    ("1.5.2","  Integration Tests",                 False, False),
    ("1.5.3","  User Acceptance Test",             False, False),
    ("1.6",  "Documentation",                        False, True),
    ("1.6.1","  User Guide",                       False, False),
    ("1.6.2","  Technical Documentation",            False, False),
    ("1.7",  "Presentation & Submission",            False, True),
    ("1.7.1","  Slide Deck",                       False, False),
    ("1.7.2","  Rehearsal",                        False, False),
]

# Left: WBS tree
for i, (wid, name, is_root, is_l2) in enumerate(wbs_items):
    ry = Inches(1.55) + i * Inches(0.215)
    indent = Inches(0.7) if is_root else (Inches(0.9) if is_l2 else Inches(1.5))
    if is_l2:
        add_rect(s, indent, ry, Inches(4.5), Inches(0.2),
                 fill=PARCH_ELEV, line=RULE, line_w=0.5)
    add_text(s, indent + Inches(0.04), ry, Inches(0.6), Inches(0.2),
             wid, font=MONO, size=8, bold=True, color=ACCENT)
    add_text(s, indent + Inches(0.6), ry, Inches(3.9), Inches(0.2),
             name, font=SANS, size=9, bold=is_l2, color=INK_SOFT if not is_l2 else INK)

# Right: hours summary
add_hline(s, Inches(6.5), Inches(1.55), Inches(6.3), RULE, Pt(0.5))
add_text(s, Inches(6.5), Inches(1.62), Inches(6.3), Inches(0.38),
         "WBS Level 3 Hours", font=SERIF, size=13, bold=True, color=INK)
hrs = [
    ("1.1 PM",  "60 h"), ("1.2 Req", "50 h"), ("1.3 Design", "80 h"),
    ("1.4 Dev", "180 h"), ("1.5 QA", "60 h"), ("1.6 Docs", "30 h"), ("1.7 Pres", "20 h"),
]
for i, (lbl, val) in enumerate(hrs):
    row = i // 2; col = i % 2
    cx = Inches(6.5) + col * Inches(3.1)
    cy = Inches(2.2) + row * Inches(0.52)
    add_rect(s, cx, cy, Inches(2.9), Inches(0.44),
             fill=PARCH_ELEV, line=RULE, line_w=0.5)
    add_text(s, cx + Inches(0.1), cy + Inches(0.03), Inches(1.6), Inches(0.36),
             lbl, font=SANS, size=9, color=MUTED)
    add_text(s, cx + Inches(1.7), cy + Inches(0.02), Inches(1.1), Inches(0.38),
             val, font=SERIF, size=13, bold=True, color=INK)

add_hline(s, Inches(6.5), Inches(4.25), Inches(6.3), RULE, Pt(0.75))
add_text(s, Inches(6.5), Inches(4.35), Inches(6.3), Inches(0.38),
         "Total Labor: 480 h × 50,000 VND/h = 24,000,000 VND",
         font=SANS, size=10, bold=True, color=INK)
add_text(s, Inches(6.5), Inches(4.78), Inches(6.3), Inches(0.28),
         "→ See Budget Rollup in Section IV",
         font=SANS, size=10, italic=True, color=MUTED)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — § III DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("III", "Timeline & Milestones", "CLO 2, 4, 5 · Ch. 4, 8, 10")
s.notes_slide.notes_text_frame.text = (
    "Section III — the schedule heart. PERT three-point estimation for six activities, "
    "full CPM forward and backward pass, critical path A→B→E→G→H, and the Gantt overview."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — GANTT (shapes)
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Timeline & Milestones", "Gantt Chart — 14-Week Timeline",
    notes=(
        "All 16 Level 3 work packages across 14 weeks. Critical path in burnt sienna — "
        "zero float. Six diamond milestones. Activity F (Backend) has 8 days of float."
    )
)

# Week headers
add_text(s, Inches(0.7), Inches(1.55), Inches(1.5), Inches(0.34),
         "WBS", font=SANS, size=8, bold=True, color=MUTED)
for w in range(1, 15):
    cx = Inches(2.35) + (w - 1) * Inches(0.76)
    add_rect(s, cx, Inches(1.55), Inches(0.73), Inches(0.34),
             fill=PARCH_ELEV, line=RULE, line_w=0.5)
    add_text(s, cx, Inches(1.55), Inches(0.73), Inches(0.34),
             f"W{w}", font=SANS, size=8, bold=True, color=INK,
             align=PP_ALIGN.CENTER)

# Gantt rows: (wid, name, start, dur, is_critical)
gantt_rows = [
    ("1.1.1","Charter & Kickoff",      1,  2, True),
    ("1.1.2","Status Meetings",          1, 14, False),
    ("1.1.3","Risk Reviews",            1, 14, False),
    ("1.2.1","Stakeholder Interviews",   2,  1, True),
    ("1.2.2","Requirements Doc",        2,  2, True),
    ("1.2.3","Req Sign-off",            3,  1, True),
    ("1.3.1","UI/UX Design",           3,  3, True),
    ("1.3.2","DB Schema",               3,  2, False),
    ("1.3.3","API Contract",            4,  2, False),
    ("1.4.1","Frontend Dev",             5,  5, True),
    ("1.4.2","Backend Dev",             5,  4, False),
    ("1.4.3","Integration",              8,  2, True),
    ("1.5.1","Unit Tests",             7,  4, False),
    ("1.5.2","Integration Tests",        9,  3, False),
    ("1.5.3","UAT",                   12,  1, False),
    ("1.6.1","User Guide",             11,  3, False),
    ("1.6.2","Tech Docs",              11,  3, False),
    ("1.7.1","Slide Deck",             12,  2, False),
    ("1.7.2","Rehearsal",              13,  2, False),
]

for i, (wid, name, start, dur, crit) in enumerate(gantt_rows):
    ry = Inches(1.95) + i * Inches(0.26)
    add_text(s, Inches(0.7), ry, Inches(0.5), Inches(0.24),
             wid, font=MONO, size=6, bold=True, color=ACCENT)
    add_text(s, Inches(1.25), ry, Inches(1.1), Inches(0.24),
             name[:16], font=SANS, size=7, color=INK)
    bx = Inches(2.35) + (start - 1) * Inches(0.76)
    bw = dur * Inches(0.76) - Inches(0.04)
    bar_fill = ACCENT if crit else RGBColor(0xC4, 0xB4, 0x9A)
    add_rect(s, bx, ry + Inches(0.04), bw, Inches(0.18),
             fill=bar_fill, line=None)

# Milestone axis
axis_y = Inches(1.95) + len(gantt_rows) * Inches(0.26) + Inches(0.08)
add_hline(s, Inches(2.35), axis_y, Inches(10.64), RULE, Pt(0.5))
milestones = [
    (1, "M1: Charter\nApproved"),
    (3, "M2: Req\nSign-off"),
    (5, "M3: Design\nReview"),
    (10,"M4: Proto\nDemo"),
    (12,"M5: Testing\nComplete"),
    (14,"M6: Final\nSubmission"),
]
for w, lbl in milestones:
    mx = Inches(2.35) + (w - 1) * Inches(0.76) + Inches(0.36)
    d = s.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, mx - Inches(0.12), axis_y + Inches(0.02),
                           Inches(0.24), Inches(0.24))
    d.fill.solid(); d.fill.fore_color.rgb = ACCENT; d.line.fill.background()
    add_text(s, mx - Inches(0.42), axis_y + Inches(0.26), Inches(0.84), Inches(0.5),
             lbl, font=SANS, size=6, italic=True, color=ACCENT, align=PP_ALIGN.CENTER)

# Legend
add_rect(s, Inches(0.7), Inches(7.07), Inches(0.28), Inches(0.18),
         fill=ACCENT, line=None)
add_text(s, Inches(1.04), Inches(7.07), Inches(1.8), Inches(0.2),
         "Critical path", font=SANS, size=8, color=INK)
add_rect(s, Inches(3.0), Inches(7.07), Inches(0.28), Inches(0.18),
         fill=RGBColor(0xC4, 0xB4, 0x9A), line=None)
add_text(s, Inches(3.34), Inches(7.07), Inches(1.5), Inches(0.2),
         "Non-critical", font=SANS, size=8, color=INK)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — PERT
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Timeline & Milestones", "PERT Three-Point Estimates",
    notes=(
        "TE = (O + 4M + P) / 6. σ = (P − O) / 6. "
        "Activity B — UI/UX Design — is the worked example: "
        "O=5, M=10, P=18 → TE=10.5d, σ=2.17d."
    )
)
pert_data = [
    ["Act.", "Description",        "O (d)", "M (d)", "P (d)", "TE = (O+4M+P)/6", "σ = (P−O)/6", "Notes"],
    ["A",    "Requirements",       "3",      "5",      "9",      "5.33 d",           "1.00 d",      "Critical path"],
    ["B",    "UI/UX Design",      "5",      "10",     "18",     "10.50 d",          "2.17 d",      "★ Worked example"],
    ["E",    "Frontend Dev",      "10",     "15",     "22",     "15.33 d",          "2.00 d",      "Critical path"],
    ["F",    "Backend Dev",       "8",      "12",     "20",     "12.67 d",          "2.00 d",      "Non-critical; 8 d float"],
    ["G",    "Integration",       "3",      "5",      "8",      "5.17 d",           "0.83 d",      "Critical path"],
    ["H",    "Testing",           "5",      "8",      "14",     "8.50 d",           "1.50 d",      "Critical path"],
]
add_table(s, pert_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(2.6),
          col_widths=[Inches(0.6), Inches(1.8), Inches(0.62), Inches(0.62),
                      Inches(0.62), Inches(1.6), Inches(1.1), Inches(2.34)],
          font_size=10,
          row_fills=[None, ACC_BG, None, None, None, None])

# Worked example box
add_rect(s, Inches(0.7), Inches(4.28), Inches(12.3), Inches(1.62),
         fill=ACC_BG, line=ACCENT, line_w=0.75)
add_text(s, Inches(0.9), Inches(4.35), Inches(6), Inches(0.38),
         "Worked Example — Activity B (UI/UX Design)",
         font=SERIF, size=12, bold=True, color=ACCENT)
calc = ("O = 5 days, M = 10 days, P = 18 days\n"
        "TE = (5 + 4×10 + 18) / 6 = 63 / 6 = 10.5 days\n"
        "σ  = (18 − 5) / 6 = 13 / 6 ≈ 2.17 days\n"
        "~68% probability of completing within 10.5 ± 2.17 days.")
add_text(s, Inches(0.9), Inches(4.78), Inches(11.9), Inches(1.05),
         calc, font=SANS, size=10, color=INK)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 12 — CPM
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Timeline & Milestones", "CPM — Forward & Backward Pass",
    notes=(
        "Forward: ES = max(EF of predecessors), EF = ES + duration. "
        "Backward: LF = min(LS of successors), LS = LF − duration. "
        "Slack = LS − ES. Critical path A→B→E→G→H = 43 days. "
        "Activity F has 8 days of float."
    )
)
cpm_data = [
    ["Act.", "Description",       "Dur.", "Pred.",  "ES", "EF", "LS", "LF", "Slack", "CP?"],
    ["A",    "Requirements",        "5 d",  "—",    "0",  "5",  "0",  "5",  "0",     "★"],
    ["B",    "UI/UX Design",       "10 d", "A",    "5",  "15", "5",  "15", "0",     "★"],
    ["C",    "DB Schema",          "4 d",  "A",    "5",  "9",  "14", "18", "9",     ""],
    ["D",    "API Design",         "5 d",  "A",    "5",  "10", "13", "18", "8",     ""],
    ["E",    "Frontend Dev",       "15 d", "B",    "15", "30", "15", "30", "0",     "★"],
    ["F",    "Backend Dev",        "12 d", "C, D", "10", "22", "18", "30", "8",     ""],
    ["G",    "Integration",        "5 d",  "E, F", "30", "35", "30", "35", "0",     "★"],
    ["H",    "Testing",            "8 d",  "G",    "35", "43", "35", "43", "0",     "★"],
]
# CP rows: 0,1,4,6,7
cp_fills = [ACC_BG if r in (0,1,4,6,7) else None for r in range(1, len(cpm_data))]
add_table(s, cpm_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(3.55),
          col_widths=[Inches(0.44), Inches(1.5), Inches(0.5), Inches(0.72),
                      Inches(0.44), Inches(0.44), Inches(0.44), Inches(0.44),
                      Inches(0.56), Inches(0.44)],
          font_size=9,
          row_fills=cp_fills)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 13 — CRITICAL PATH
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Timeline & Milestones", "The Critical Path",
    accent_title=True,
    notes=(
        "A → B → E → G → H = 43 working days, ~9 calendar weeks. "
        "Activity F — Backend Dev — has 8 days of float. "
        "The project duration is dominated by Frontend Dev at 15 days."
    )
)
add_hline(s, Inches(0.7), Inches(1.82), Inches(12.3), RULE, Pt(0.75))

path = [
    ("A", "Requirements\n5 days"),
    ("B", "UI/UX Design\n10 days"),
    ("E", "Frontend Dev\n15 days"),
    ("G", "Integration\n5 days"),
    ("H", "Testing\n8 days"),
]
for i, (node, lbl) in enumerate(path):
    cx = Inches(0.7) + i * Inches(2.5)
    add_rect(s, cx, Inches(2.0), Inches(2.1), Inches(1.42),
             fill=ACCENT, line=ACCENT, line_w=1)
    add_text(s, cx, Inches(2.05), Inches(2.1), Inches(0.7),
             node, font=SERIF, size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, cx + Inches(0.05), Inches(2.75), Inches(2.0), Inches(0.6),
             lbl, font=SANS, size=10, color=WHITE, align=PP_ALIGN.CENTER)
    if i < len(path) - 1:
        add_text(s, cx + Inches(2.1), Inches(2.42), Inches(0.4), Inches(0.6),
                 "→", font=SANS, size=26, color=ACCENT)

add_hline(s, Inches(0.7), Inches(3.62), Inches(12.3), RULE, Pt(0.75))
add_text(s, Inches(0.7), Inches(3.72), Inches(12.3), Inches(0.58),
         "A → B → E → G → H  =  5 + 10 + 15 + 5 + 8  =  43 working days",
         font=SERIF, size=20, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
add_text(s, Inches(0.7), Inches(4.38), Inches(12.3), Inches(0.38),
         "≈ 9 calendar weeks  ·  Activity F (Backend Dev) has 8 days of float",
         font=SANS, size=12, italic=True, color=INK_SOFT, align=PP_ALIGN.CENTER)

float_data = [
    ["Activity",          "Slack",   "Interpretation"],
    ["F — Backend Dev",  "8 days",  "Can slip up to 8 days without delaying project"],
    ["D — API Design",   "8 days",  "Can slip up to 8 days"],
    ["C — DB Schema",    "9 days",  "Can slip up to 9 days"],
]
add_table(s, float_data,
          Inches(0.7), Inches(5.0), Inches(8.5), Inches(1.6),
          col_widths=[Inches(2.0), Inches(1.0), Inches(5.5)],
          font_size=10)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 14 — § IV DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("IV", "Resource Management", "CLO 2, 8, 9 · Ch. 5, 11, 12")
s.notes_slide.notes_text_frame.text = (
    "Section IV — RACI matrix, make-or-buy analysis, and bottom-up budget totalling 33.6 million VND."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 15 — RACI
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Resource Management", "RACI Matrix — Responsibility Assignment",
    notes=(
        "One Accountable per row, at least one Responsible per row, "
        "no member is exclusively Informed. Each of our four members carries A+R roles."
    )
)
raci_data = [
    ["Work Package",        "WBS",   "Đức (PM)", "Bảo (Dev)", "Thịnh (UI/UX)", "Hiếu (QA)"],
    ["Project Planning",     "1.1.1", "A",         "C",           "I",             "I"],
    ["Requirements",         "1.2",   "A",         "R",           "R",             "C"],
    ["UI/UX Design",        "1.3.1", "I",         "C",           "A/R",           "I"],
    ["DB Schema",            "1.3.2", "A",         "R",           "I",             "C"],
    ["API Design",           "1.3.3", "A",         "R",           "I",             "I"],
    ["Frontend Dev",         "1.4.1", "C",         "C",           "A/R",           "I"],
    ["Backend Dev",          "1.4.2", "I",         "A/R",         "I",             "C"],
    ["Unit Testing",         "1.5.1", "I",         "C",           "I",             "A/R"],
    ["Documentation",        "1.6",   "C",         "C",           "C",             "A/R"],
    ["Presentation",         "1.7",   "A",         "R",           "R",             "R"],
]
add_table(s, raci_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(4.2),
          col_widths=[Inches(2.1), Inches(0.55), Inches(1.55), Inches(1.55),
                      Inches(1.7), Inches(1.55)],
          font_size=9)
add_text(s, Inches(0.7), Inches(5.92), Inches(12), Inches(0.3),
         "R = Responsible  ·  A = Accountable  ·  C = Consulted  ·  I = Informed",
         font=SANS, size=9, italic=True, color=MUTED)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 16 — BUDGET
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Resource Management", "Bottom-Up Budget Rollup",
    accent_title=True,
    notes=(
        "Hours × 50,000 VND/h → labor 24M → +20% OH + G&A + Contingency + Mgmt reserve. "
        "G&A reduced from 2.4M to 1.72M to fund the 680K management reserve needed "
        "to cover the full EMV of 3.08M. BAC stays at 33.6M."
    )
)
budget_data = [
    ["WBS", "Work Package",                "Hours", "Cost (VND)"],
    ["1.1",  "Project Management",          "60",   "3,000,000"],
    ["1.2",  "Requirements & Analysis",      "50",   "2,500,000"],
    ["1.3",  "System Design",               "80",   "4,000,000"],
    ["1.4",  "Development",                 "180",   "9,000,000"],
    ["1.5",  "Testing & QA",                "60",   "3,000,000"],
    ["1.6",  "Documentation",                "30",   "1,500,000"],
    ["1.7",  "Presentation & Submission",  "20",   "1,000,000"],
    ["LABOR","Subtotal (480 h × 50K)",     "480",  "24,000,000"],
    ["",     "+ Overhead 20%",              "",     "4,800,000"],
    ["",     "+ G&A 10% (reallocated)",    "",     "1,720,000"],
    ["",     "+ Contingency 10%",            "",     "2,400,000"],
    ["",     "+ Management Reserve",          "",       "680,000"],
    ["BAC",  "Budget at Completion",         "",     "33,600,000 VND"],
]
row_fills = [None]*7 + [PARCH_ELEV] + [None]*4 + [ACC_BG]
add_table(s, budget_data,
          Inches(0.7), Inches(1.55), Inches(8.5), Inches(5.3),
          col_widths=[Inches(0.58), Inches(3.4), Inches(0.72), Inches(2.0)],
          font_size=9,
          row_fills=row_fills)

# Big BAC callout
add_rect(s, Inches(9.5), Inches(1.55), Inches(3.5), Inches(2.2),
         fill=ACCENT, line=ACCENT, line_w=1)
add_text(s, Inches(9.6), Inches(1.65), Inches(3.3), Inches(0.5),
         "BAC", font=SERIF, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(9.6), Inches(2.15), Inches(3.3), Inches(0.8),
         "33,600,000", font=SERIF, size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(9.6), Inches(2.95), Inches(3.3), Inches(0.4),
         "VND", font=SANS, size=13, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(9.6), Inches(3.42), Inches(3.3), Inches(0.3),
         "480 h × 50,000/h\n+ overhead + contingency",
         font=SANS, size=8, italic=True, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 17 — PV CURVE
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Resource Management", "Time-Phased Budget — Planned Value Curve",
    notes=(
        "PV curve: front-loaded during development months 4-7. "
        "Cumulative spend reaches BAC of 33.6M at month 8. "
        "Locked as the EVM cost baseline at Week 1."
    )
)

pv_data = [
    ("M1",  8,   2_688_000),
    ("M2",  15,  5_040_000),
    ("M3",  25,  8_400_000),
    ("M4",  40, 13_440_000),
    ("M5",  55, 18_480_000),
    ("M6",  70, 23_520_000),
    ("M7",  85, 28_560_000),
    ("M8", 100, 33_600_000),
]

chart_l = _I(Inches(0.7)); chart_t = _I(Inches(1.55))
chart_w = _I(Inches(9.5)); chart_h = _I(Inches(4.8))
axis_x = chart_l + _I(Inches(0.5)); axis_y = chart_t + chart_h - _I(Inches(0.5))
bar_area_w = chart_w - _I(Inches(0.6)); bar_area_h = chart_h - _I(Inches(0.7))
n = len(pv_data)

add_hline(s, axis_x, axis_y, bar_area_w, INK, Pt(0.75))
add_vline(s, axis_x, axis_y - bar_area_h, bar_area_h, INK, Pt(0.75))

for pct in [0, 25, 50, 75, 100]:
    y = axis_y - (pct * bar_area_h) // 100
    add_text(s, axis_x - _I(Inches(0.46)), y - _I(Inches(0.13)), _I(Inches(0.42)), _I(Inches(0.24)),
             f"{pct}%", font=SANS, size=8, color=MUTED, align=PP_ALIGN.RIGHT)
    add_hline(s, axis_x, y, bar_area_w, RULE, Pt(0.3))

# Bar width — must be a plain int
bar_w = (bar_area_w - (n - 1) * _I(Inches(0.14))) // n
for i, (month, pct, vnd) in enumerate(pv_data):
    bh = (pct * bar_area_h) // 100
    bx = axis_x + i * (bar_w + _I(Inches(0.14)))
    by = axis_y - bh
    add_rect(s, bx, by, bar_w, bh,
             fill=ACCENT if pct == 100 else INK_SOFT, line=None)
    add_text(s, bx, by - Inches(0.32), bar_w, Inches(0.3),
             f"{vnd//1000:,}K",
             font=MONO, size=7, color=INK, align=PP_ALIGN.CENTER)
    add_text(s, bx, axis_y + Inches(0.02), bar_w, Inches(0.24),
             month, font=SANS, size=8, color=INK, align=PP_ALIGN.CENTER)

# Data table
tbl_data = [
    ["Month", "PV (VND)",    "%"],
    ["M1",   "2,688,000",  "8%"],
    ["M2",   "5,040,000",  "15%"],
    ["M3",   "8,400,000",  "25%"],
    ["M4",   "13,440,000", "40%"],
    ["M5",   "18,480,000", "55%"],
    ["M6",   "23,520,000", "70%"],
    ["M7",   "28,560,000", "85%"],
    ["M8",   "33,600,000", "100%"],
]
add_table(s, tbl_data,
          Inches(10.4), Inches(1.55), Inches(2.6), Inches(3.0),
          col_widths=[Inches(0.6), Inches(1.15), Inches(0.85)],
          font_size=9)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 18 — § V DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("V", "Risk Management", "CLO 3, 6 · Ch. 7")
s.notes_slide.notes_text_frame.text = (
    "Section V — six risks, EMV calculations, heatmap, and mitigation planning. "
    "Total cost EMV of 3.08M drives our contingency reserve."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 19 — RISK REGISTER
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Risk Management", "Risk Register — 6 Risks with EMV",
    notes=(
        "Six risks identified through team brainstorming. EMV = Likelihood × Impact. "
        "R2 scope creep has highest EMV at 1.5M VND. "
        "Total EMV cost 3.08M, time EMV 13.35 days."
    )
)
risk_data = [
    ["ID", "Risk Description",                    "Cat.",  "L",   "Cost Impact", "Time Impact", "EMV Cost",    "EMV Time",  "Strategy",               "Owner"],
    ["R1", "Member unavailable (illness/conflict)", "People","0.30","1,000,000",  "5 d",        "300,000",    "1.50 d",    "Contingency / Accept",   "Đức"],
    ["R2", "Scope creep — new requirements added",  "Scope", "0.50","3,000,000",  "10 d",       "1,500,000",  "5.00 d",    "Avoid + Reduce",         "Đức"],
    ["R3", "Stack unfamiliarity (React 19, TS)",   "Tech",  "0.40","500,000",    "7 d",        "200,000",    "2.80 d",    "Reduce",                 "Bảo"],
    ["R4", "Data loss / version control failure",   "Tech",  "0.15","2,000,000",  "3 d",        "300,000",    "0.45 d",    "Reduce",                 "Thịnh"],
    ["R5", "FE/BE integration failure at W7",      "Tech",  "0.35","2,000,000",  "8 d",        "700,000",    "2.80 d",    "Reduce",                 "Hiếu"],
    ["R6", "Meeting coordination issues",          "People","0.40","200,000",    "2 d",        "80,000",     "0.80 d",    "Accept",                 "Đức"],
    ["",   "TOTAL EMV",                             "",      "",    "",            "",           "3,080,000 VND","13.35 d",  "",                        ""],
]
add_table(s, risk_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(3.3),
          col_widths=[Inches(0.36), Inches(2.28), Inches(0.62), Inches(0.42),
                      Inches(0.84), Inches(0.64), Inches(0.84), Inches(0.64),
                      Inches(1.4), Inches(0.64)],
          font_size=8,
          row_fills=[None]*5 + [PARCH_ELEV] + [ACC_BG])


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 20 — HEATMAP
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Risk Management", "Risk Heatmap — Likelihood × Impact",
    notes=(
        "3×3 grid: likelihood vs impact. High zone: R2, R3, R5 need active mitigation. "
        "Medium zone: R1 and R6 monitored. Low zone: R4 accepted with preventive measures."
    )
)

zone_fill = {
    (3,3): WARN,       (3,2): RGBColor(0xC4,0x9A,0x7A), (3,1): ACC_BG,
    (2,3): RGBColor(0xC4,0x9A,0x7A), (2,2): RULE, (2,1): PARCHMENT,
    (1,3): ACC_BG, (1,2): PARCHMENT, (1,1): PARCHMENT,
}

cell_w = Inches(2.3); cell_h = Inches(1.2)
grid_l = Inches(1.5); grid_t = Inches(1.55)

add_text(s, Inches(0.4), Inches(3.5), Inches(0.9), Inches(0.3),
         "LIKELIHOOD →", font=SANS, size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
add_text(s, Inches(3.2), Inches(6.58), Inches(2.0), Inches(0.3),
         "IMPACT →", font=SANS, size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)

for row in range(1, 4):
    for col in range(1, 4):
        cx = grid_l + (col - 1) * cell_w
        cy = grid_t + (3 - row) * cell_h
        add_rect(s, cx, cy, cell_w - Inches(0.04), cell_h - Inches(0.04),
                 fill=zone_fill[(row, col)], line=RULE, line_w=0.5)

risks = [
    (3,3,"R2", ACCENT), (3,2,"R3", ACCENT), (2,3,"R5", ACCENT),
    (2,2,"R1", INK_SOFT), (2,2,"R6", INK_SOFT), (1,1,"R4", MUTED),
]
for (l, i, lbl, col) in risks:
    cx = grid_l + (i - 1) * cell_w + cell_w // 2 - _I(Inches(0.2))
    cy = grid_t + (3 - l) * cell_h + cell_h // 2 - _I(Inches(0.2))
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, Inches(0.38), Inches(0.38))
    circ.fill.solid(); circ.fill.fore_color.rgb = col
    circ.line.color.rgb = WHITE; circ.line.width = Pt(1)
    add_text(s, cx, cy, Inches(0.38), Inches(0.38),
             lbl, font=SANS, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(s, grid_l + Inches(1.5), grid_t + Inches(2.48), Inches(2.5), Inches(0.28),
         "HIGH RISK", font=SANS, size=8, bold=True, color=WARN, align=PP_ALIGN.CENTER)
add_text(s, grid_l + Inches(1.5), grid_t + Inches(1.28), Inches(2.5), Inches(0.28),
         "MEDIUM", font=SANS, size=8, color=MUTED, align=PP_ALIGN.CENTER)
add_text(s, grid_l + Inches(1.5), grid_t + Inches(0.08), Inches(2.5), Inches(0.28),
         "LOW RISK", font=SANS, size=8, color=OK, align=PP_ALIGN.CENTER)

leg_data = [
    ["Risk", "L",  "Impact",  "Zone"],
    ["R1 — Member unavailable",  "0.30","5 d",   "Medium"],
    ["R2 — Scope creep",      "0.50","10 d",  "High"],
    ["R3 — Stack unfamiliarity","0.40","7 d",   "High"],
    ["R4 — Data loss",         "0.15","3 d",   "Low"],
    ["R5 — Integration fail",  "0.35","8 d",   "High"],
    ["R6 — Meeting issues",     "0.40","2 d",   "Medium"],
]
add_table(s, leg_data,
          Inches(8.5), Inches(1.55), Inches(4.5), Inches(2.8),
          col_widths=[Inches(2.0), Inches(0.5), Inches(0.6), Inches(1.4)],
          font_size=8)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 21 — EMV RECONCILIATION
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Risk Management", "EMV Reconciliation",
    accent_title=True,
    notes=(
        "Contingency 2.4M alone doesn't cover EMV 3.08M. "
        "Gap of 680K funded by reallocating from G&A. "
        "BAC unchanged at 33.6M — reserves reallocated, not added."
    )
)
recon_data = [
    ["Item",                                        "Amount (VND)", "Notes"],
    ["Total Risk EMV (cost)",                       "3,080,000",    "From risk register Table 14"],
    ["Contingency reserve (10% of labor)",           "2,400,000",    "From budget baseline"],
    ["Gap (EMV − Contingency)",                    "680,000",      "EMV exceeds contingency"],
    ["Management reserve (from G&A buffer)",       "+ 680,000",    "Drawn from G&A; approved by PM"],
    ["Adjusted G&A (reduced from 2,400,000)",      "1,720,000",    "G&A reduced by 680,000"],
    ["TOTAL RISK COVERAGE",                          "3,080,000 VND","Full EMV covered ✓"],
    ["Budget at Completion (unchanged)",             "33,600,000",   "Total budget unchanged"],
]
add_table(s, recon_data,
          Inches(0.7), Inches(1.55), Inches(8.0), Inches(3.9),
          col_widths=[Inches(3.5), Inches(1.8), Inches(2.7)],
          font_size=10,
          row_fills=[None]*3 + [RGBColor(0xF0,0xE9,0xDD)] + [None]*2 + [ACC_BG])

add_rect(s, Inches(9.0), Inches(1.55), Inches(4.0), Inches(2.0),
         fill=ACCENT, line=ACCENT, line_w=1)
add_text(s, Inches(9.1), Inches(1.65), Inches(3.8), Inches(0.45),
         "EMV = Contingency + Mgmt Reserve",
         font=SANS, size=10, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(9.1), Inches(2.1), Inches(3.8), Inches(0.7),
         "3,080,000", font=SERIF, size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(9.1), Inches(2.8), Inches(3.8), Inches(0.3),
         "VND", font=SANS, size=12, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(9.1), Inches(3.12), Inches(3.8), Inches(0.28),
         "= 2,400,000 + 680,000",
         font=SANS, size=10, italic=True, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 22 — § VI DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("VI", "Communication & Collaboration",
                    "CLO 4, 5, 8, 9, 12 · Ch. 9, 11, 12")
s.notes_slide.notes_text_frame.text = (
    "Section VI — how the team communicates and resolves conflict. "
    "6-step process for interpersonal issues, formal change control for scope changes."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 23 — CONFLICT + STAKEHOLDER
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Communication", "Conflict Resolution & Stakeholder Strategy",
    notes=(
        "6-step conflict resolution: focus on issues not personalities, document agreements. "
        "Stakeholder power/interest grid: instructors are high power/high interest."
    )
)

# Left: 6 steps
add_text(s, Inches(0.7), Inches(1.55), Inches(6.0), Inches(0.38),
         "6-Step Conflict Resolution", font=SERIF, size=15, bold=True, color=INK)
steps = [
    ("1", "Identify root causes",
     "PM calls private session; each party states position in one sentence"),
    ("2", "Gather facts",
     "Review task logs, commit history, WBS — no hearsay"),
    ("3", "Facilitate open discussion",
     "Moderated by PM; time-boxed to 15 min per issue"),
    ("4", "Focus on issues, not personalities",
     "PM enforces ground rules; redirect from 'you' to 'the decision'"),
    ("5", "Seek win-win resolutions",
     "Explore trade-offs; document rationale"),
    ("6", "Document agreements",
     "Added to meeting minutes within 24 h; all parties confirm via Teams"),
]
for i, (num, title, desc) in enumerate(steps):
    sy = Inches(2.02) + i * Inches(0.8)
    add_rect(s, Inches(0.7), sy, Inches(0.4), Inches(0.68),
             fill=ACCENT, line=None)
    add_text(s, Inches(0.7), sy, Inches(0.4), Inches(0.68),
             num, font=SERIF, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, Inches(1.2), sy, Inches(2.0), Inches(0.3),
             title, font=SANS, size=10, bold=True, color=INK)
    add_text(s, Inches(1.2), sy + Inches(0.28), Inches(5.3), Inches(0.38),
             desc, font=SANS, size=9, color=INK_SOFT)

# Right: Power/Interest grid
add_text(s, Inches(7.5), Inches(1.55), Inches(5.5), Inches(0.38),
         "Stakeholder Power / Interest Grid", font=SERIF, size=15, bold=True, color=INK)
grid_data = [
    ["",                    "Low Interest",    "High Interest"],
    ["High\nPower",         "Monitor\n(Peer Groups)",  "Keep Satisfied\n(Instructor, Univ.)"],
    ["Low\nPower",          "Keep Informed\n(Bystanders)", "Keep Informed\n(End Users)"],
]
stake_t = s.shapes.add_table(3, 3, Inches(7.5), Inches(2.0),
                           Inches(5.4), Inches(3.5)).table
fills = [ACCENT, PARCHMENT, PARCH_ELEV]
st_row = [RGBColor(0xF0,0xE9,0xDD), OK, ACC_BG]
nd_row = [RGBColor(0xF0,0xE9,0xDD), PARCHMENT, RGBColor(0xE8,0xD5,0xBC)]
for r, row in enumerate(grid_data):
    for c, val in enumerate(row):
        cell = stake_t.cell(r, c)
        cell.margin_left = Inches(0.1); cell.margin_right = Inches(0.1)
        cell.margin_top = Inches(0.05); cell.margin_bottom = Inches(0.05)
        cell.text = ""
        p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        run = p.add_run(); run.text = val
        run.font.name = SANS; run.font.size = Pt(9)
        run.font.color.rgb = WHITE if r == 0 else INK
        cell.fill.solid()
        if r == 0:
            cell.fill.fore_color.rgb = ACCENT
        elif r == 1:
            cell.fill.fore_color.rgb = st_row[c]
        else:
            cell.fill.fore_color.rgb = nd_row[c]


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 24 — § VII DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("VII", "Monitoring & EVM", "CLO 7 · Ch. 10")
s.notes_slide.notes_text_frame.text = (
    "Section VII — Earned Value Management. Week 6 snapshot: CPI=0.75, SPI≈0.45. "
    "Project is over budget and behind schedule. Corrective action planned."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 25 — EVM WEEK 6
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Monitoring & EVM", "EVM Status — Week 6 Snapshot",
    accent_title=True,
    notes=(
        "EV of 7.5M from completed milestones. AC of 10M from 200 logged hours. "
        "PV at W6 should be 16.8M (50% of BAC). "
        "CV −2.5M, SV −9.3M, CPI 0.75, SPI 0.45, EAC 44.8M."
    )
)
evm_kpis = [
    ("0.75",    "Cost Performance\nIndex (CPI)",    "Over budget"),
    ("0.45",    "Schedule Perf.\nIndex (SPI)",      "Behind schedule"),
    ("44.8M",   "Est. at Completion\n(EAC)",        "Forecast: +11.2M"),
    ("−2.5M",   "Cost Variance\n(CV)",               "Over budget by 2.5M"),
    ("−11.2M",  "Variance at\nCompletion (VAC)",     "Forecast overrun"),
]
for i, (val, lbl, sub) in enumerate(evm_kpis):
    cx = Inches(0.7) + i * Inches(2.5)
    kpi_card(s, cx, Inches(1.55), Inches(2.36), Inches(1.72), lbl, val, sub, accent=(i==0))

evm_data = [
    ["Metric","Formula",                      "Workings",                           "Value"],
    ["BAC",   "Budget at Completion",         "From budget baseline",             "33,600,000 VND"],
    ["PV",    "Planned Value at W6",          "50% of BAC",                       "16,800,000 VND"],
    ["EV",    "Earned Value",                   "M1+M2+M3+partial = 7.5M",        "7,500,000 VND"],
    ["AC",    "Actual Cost",                    "200 h × 50,000 VND/h",            "10,000,000 VND"],
    ["CV",    "Cost Variance",                  "EV − AC = 7.5M − 10M",           "−2,500,000 VND"],
    ["SV",    "Schedule Variance",               "EV − PV = 7.5M − 16.8M",         "−9,300,000 VND"],
    ["CPI",   "Cost Perf. Index",               "EV / AC = 7.5M / 10M",            "0.75"],
    ["SPI",   "Schedule Perf. Index",            "EV / PV = 7.5M / 16.8M",          "≈ 0.45"],
    ["EAC",   "Estimate at Completion",          "BAC / CPI = 33.6M / 0.75",        "44,800,000 VND"],
    ["ETC",   "Estimate to Complete",            "EAC − AC = 44.8M − 10M",         "34,800,000 VND"],
    ["VAC",   "Variance at Completion",          "BAC − EAC = 33.6M − 44.8M",      "−11,200,000 VND"],
]
add_table(s, evm_data,
          Inches(0.7), Inches(3.42), Inches(12.3), Inches(3.6),
          col_widths=[Inches(0.7), Inches(2.0), Inches(4.1), Inches(2.0)],
          font_size=9,
          row_fills=[None]*4 + [WARN]*2 + [None]*5 + [WARN])


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 26 — ISSUE LOG + CHANGE CONTROL
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Monitoring & EVM", "Issue Log & Change Control",
    notes=(
        "ISS-001: stakeholder interviews ran +3h, closed. ISS-002: react-router-dom v7 "
        "broke the build, downgraded to v6, closed. ISS-003: integration milestone at risk, open. "
        "CR-001 approved replacing Supabase with local state — positive schedule, minor cost saving."
    )
)
add_text(s, Inches(0.7), Inches(1.55), Inches(5.8), Inches(0.38),
         "Issue Log", font=SERIF, size=14, bold=True, color=INK)
issue_data = [
    ["ID",     "Week", "Description",                        "Owner","Status"],
    ["ISS-001","W3",   "Stakeholder interviews took +3 h",   "Đức",  "Closed"],
    ["ISS-002","W5",   "react-router-dom v7 routing broken",   "Bảo",  "Closed"],
    ["ISS-003","W6",   "M4 Integration milestone at risk",   "Đức",  "Open"],
]
add_table(s, issue_data,
          Inches(0.7), Inches(2.0), Inches(5.8), Inches(1.9),
          col_widths=[Inches(0.64), Inches(0.5), Inches(3.0), Inches(0.64), Inches(0.64)],
          font_size=9,
          row_fills=[None, RGBColor(0xE8,0xF0,0xE4), RGBColor(0xE8,0xF0,0xE4), RGBColor(0xF5,0xE9,0xDD)])

add_text(s, Inches(6.8), Inches(1.55), Inches(6.2), Inches(0.38),
         "Change Request CR-001", font=SERIF, size=14, bold=True, color=INK)
cr_data = [
    ["Field",        "Value"],
    ["Date",         "Week 6"],
    ["Requester",    "Bảo"],
    ["Description",  "Replace Supabase (cloud) with local state + mock data"],
    ["Impact — Time","+1 day float recovered; no schedule impact"],
    ["Impact — Cost","−200,000 VND (eliminates Supabase setup)"],
    ["Impact — Scope","Removes cloud sync; already in Out-of-Scope"],
    ["Decision",      "APPROVED"],
    ["Status",        "IMPLEMENTED"],
]
add_table(s, cr_data,
          Inches(6.8), Inches(2.0), Inches(6.2), Inches(3.7),
          col_widths=[Inches(1.6), Inches(4.6)],
          font_size=9,
          row_fills=[None]*7 + [OK, OK])


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 27 — § VIII DIVIDER
# ═══════════════════════════════════════════════════════════════════════════
s = section_divider("VIII", "Prototype & Lessons", "CLO 7, 8, 9 · Ch. 13")
s.notes_slide.notes_text_frame.text = (
    "Section VIII — live demo plan for three features, five lessons learned, "
    "and full CLO coverage confirmation."
)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 28 — DEMO PLAN
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Prototype & Lessons", "Prototype Demonstration Plan",
    notes=(
        "Three features in under 3 minutes. Feature 1: task CRUD + assignment. "
        "Feature 2: deadline management with overdue highlight. "
        "Feature 3: progress dashboard with live metrics. Demo URL localhost:5173."
    )
)
features = [
    ("Feature 1", "Task CRUD +\nAssignment",     "90 s",
     "Navigate to /tasks\nCreate task: assign to 'Bảo',\nset deadline June 20, priority High\n→ Verify assignee badge appears",
     "WBS 1.4.1", "Bảo + Thịnh"),
    ("Feature 2", "Deadline Management\n+ Overdue Highlight", "60 s",
     "Show task with past deadline\n(yesterday: June 15)\n→ Red overdue badge displayed\n→ Filter by 'Overdue'",
     "WBS 1.3.1", "Thịnh"),
    ("Feature 3", "Progress Dashboard", "60 s",
     "Navigate to /dashboard\n→ Project cards with counts\n→ Task progress bar (e.g. 60%)\n→ Real-time metric aggregation",
     "WBS 1.4.1, 1.4.2", "Bảo"),
]
cols = [Inches(0.7), Inches(4.7), Inches(8.7)]
for i, (feat, title, time, script, wbs, owner) in enumerate(features):
    cx = cols[i]
    add_rect(s, cx, Inches(1.55), Inches(3.8), Inches(0.44),
             fill=ACCENT, line=None)
    add_text(s, cx, Inches(1.55), Inches(3.8), Inches(0.44),
             f"{feat}  ·  {time}",
             font=SANS, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, cx, Inches(2.04), Inches(3.8), Inches(4.5),
             fill=PARCH_ELEV, line=RULE, line_w=0.75)
    add_text(s, cx + Inches(0.1), Inches(2.1), Inches(3.6), Inches(0.62),
             title, font=SERIF, size=13, bold=True, color=ACCENT)
    add_text(s, cx + Inches(0.1), Inches(2.78), Inches(3.6), Inches(0.28),
             "Script:", font=SANS, size=9, bold=True, color=MUTED)
    add_text(s, cx + Inches(0.1), Inches(3.08), Inches(3.6), Inches(2.0),
             script, font=SANS, size=9, color=INK)
    add_text(s, cx + Inches(0.1), Inches(5.52), Inches(3.6), Inches(0.28),
             f"WBS: {wbs}", font=SANS, size=9, color=MUTED)
    add_text(s, cx + Inches(0.1), Inches(5.86), Inches(3.6), Inches(0.28),
             f"Owner: {owner}", font=SANS, size=9, color=MUTED)

add_text(s, Inches(0.7), Inches(7.02), Inches(12.3), Inches(0.28),
         "Demo URL: http://localhost:5173  ·  Run: npm install && npm run dev",
         font=SANS, size=10, italic=True, color=MUTED)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 29 — LESSONS LEARNED
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Prototype & Lessons", "Lessons Learned",
    notes=(
        "LL-1: scope creep at W6 — formal scope lock via CR-001. "
        "LL-2: PERT estimates too optimistic — use 1.2× multiplier for design. "
        "LL-3: react-router v7 broke build — pin versions in package.json. "
        "LL-4: EVM reactive — implement weekly mini-checks. "
        "LL-5: no frozen API contract — parallel dev caused 2 days rework. Freeze API at W5."
    )
)
ll_data = [
    ["ID",    "Lesson",                            "Evidence / Action",                          "CLO"],
    ["LL-1",  "Scope creep at W6",                 "CR-001 formalised scope lock; 4 h recovered",  "CLO 3, 9"],
    ["LL-2",  "PERT estimates too optimistic",      "Activity B took 14 d; TE=10.5. Use 1.2×.",   "CLO 2, 5"],
    ["LL-3",  "react-router v7 incompatibility",    "Downgraded to v6; pin versions in package.json", "CLO 3, 5"],
    ["LL-4",  "EVM was reactive, not proactive",   "VAC=−11.2M. Weekly EVM mini-check.",           "CLO 6, 7"],
    ["LL-5",  "No frozen API contract",             "2 days rework at W7. Freeze API at W5.",        "CLO 2, 4"],
]
add_table(s, ll_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(3.1),
          col_widths=[Inches(0.56), Inches(2.2), Inches(6.78), Inches(0.88)],
          font_size=10)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 30 — CLO COVERAGE
# ═══════════════════════════════════════════════════════════════════════════
s = content_slide(
    "Prototype & Lessons", "CLO Coverage Matrix — All 9 CLOs",
    notes=(
        "All nine INS3044 Course Learning Outcomes demonstrably covered. "
        "CLO 1 through CLO 9 map to specific sections and evidence artefacts."
    )
)
clo_data = [
    ["CLO",   "Description",                                    "Section",  "Evidence"],
    ["CLO 1", "APPLY PM principles",                            "§ 1",     "SMART objectives; full PM cycle"],
    ["CLO 2", "IMPLEMENT scope / HR / time / cost",           "§ 1–4",   "WBS, CPM, RACI, bottom-up budget"],
    ["CLO 3", "IMPLEMENT integration / risk / quality",       "§ 5, § 8","Risk EMV; quality metrics; CR-001"],
    ["CLO 4", "IMPLEMENT systems & decisions",                 "§ 6, § 8","Decision process; live demo"],
    ["CLO 5", "USE tools / processes / techniques",            "§ 2–3",   "WBS tool, MS Project, PERT/CPM"],
    ["CLO 6", "PERFORM risk analysis & contingency",           "§ 5",      "6 risks; EMV; contingency reconciliation"],
    ["CLO 7", "PERFORM overall evaluation",                    "§ 7",      "10 EVM metrics; 5 lessons tagged"],
    ["CLO 8", "IMPLEMENT overall project plans",              "All",      "Report is the project plan; ZIP package"],
    ["CLO 9", "Autonomy & personal qualities",                  "§ 6, § 8","4 members with A/R roles; conflict process"],
]
add_table(s, clo_data,
          Inches(0.7), Inches(1.55), Inches(12.3), Inches(4.2),
          col_widths=[Inches(0.66), Inches(3.2), Inches(0.8), Inches(3.2)],
          font_size=9)
add_hline(s, Inches(0.7), Inches(5.92), Inches(12.3), RULE, Pt(0.75))
add_text(s, Inches(0.7), Inches(6.02), Inches(12.3), Inches(0.38),
         "Coverage check: All 9 CLOs demonstrably addressed through specific report sections and evidence. ✓",
         font=SANS, size=11, bold=True, color=OK)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 31 — THANK YOU
# ═══════════════════════════════════════════════════════════════════════════
sn = nxt()
s = prs.slides.add_slide(blank)
set_bg(s, PARCHMENT)
add_hline(s, Inches(0), Inches(0.04), SW, RULE, Pt(1))

add_text(s, Inches(0.9), Inches(1.2), Inches(11.5), Inches(1.4),
         "Thank you", font=SERIF, size=68, bold=True, italic=True, color=INK)
add_text(s, Inches(0.9), Inches(2.7), Inches(11.5), Inches(0.68),
         "Questions & Discussion",
         font=SERIF, size=30, italic=True, color=INK_SOFT)
add_hline(s, Inches(0.9), Inches(3.48), Inches(11.533), RULE, Pt(1))
add_text(s, Inches(0.9), Inches(3.62), Inches(11.5), Inches(0.38),
         "Group 14 · INS3044 IT Project Management",
         font=SANS, size=13, color=MUTED)

for i, (role, name, sid) in enumerate(members):
    cx = Inches(0.9) + i * (card_w + card_gap)
    add_rect(s, cx, Inches(4.12), card_w, Inches(1.1),
             fill=PARCH_ELEV, line=RULE, line_w=0.75)
    add_text(s, cx + Inches(0.1), Inches(4.17), Inches(2.5), Inches(0.28),
             role, font=SANS, size=9, color=MUTED)
    add_text(s, cx + Inches(0.1), Inches(4.42), Inches(2.5), Inches(0.32),
             name, font=SERIF, size=13, bold=True, color=INK)
    add_text(s, cx + Inches(0.1), Inches(4.8), Inches(2.5), Inches(0.28),
             sid, font=SANS, size=10, color=MUTED)

add_hline(s, Inches(0.9), Inches(5.52), Inches(11.533), RULE, Pt(0.75))
add_text(s, Inches(0.9), Inches(5.62), Inches(11.5), Inches(0.38),
         "Nguyễn Long Đức (23070435) · Phạm Hồ Bảo (23070455) · "
         "Kiều Bá Thịnh (23070247) · Đỗ Huy Hiếu (23070325)",
         font=SANS, size=10, color=INK_SOFT)
add_text(s, Inches(0.9), Inches(6.05), Inches(11.5), Inches(0.28),
         "Faculty of Applied Sciences · Vietnam National University · June 2026",
         font=SANS, size=10, color=MUTED)
add_text(s, Inches(12.3), Inches(7.27), Inches(1), Inches(0.28),
         f"{sn:02d} / {TOTAL:02d}",
         font=MONO, size=9, color=MUTED, align=PP_ALIGN.RIGHT)

s.notes_slide.notes_text_frame.text = (
    "Thank you for your attention. All four team members can answer questions in their "
    "respective areas: Đức on schedule and risk, Bảo on technical implementation, "
    "Thịnh on design and UX, Hiếu on testing and quality. "
    "Full report, prototype, and presentation materials are in the submission ZIP."
)


# ── Save ──────────────────────────────────────────────────────────────────
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "Group14_INS3044_Cartesian.pptx")
prs.save(out_path)
print(f"Saved: {out_path}")
print(f"Slides: {len(prs.slides)}")
