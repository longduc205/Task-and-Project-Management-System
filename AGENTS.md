# AGENTS.md — Project Memory

This file is automatically consulted by AI agents at the start of every session in this workspace.
Lessons here are workspace-specific knowledge that supplements the always-applied rules in
`.cursor/rules/`.

---

## Learned Workspace Facts

- The user has a `docs/slides/build_pptx.py` script at `/Users/azure_awabi/Downloads/Task-and-Project-Management-System/docs/slides/build_pptx.py` that produces `Group14_INS3044_Cartesian.pptx` for the INS3044 final project. When working on the deck, modify this script and re-run it — never edit the `.pptx` directly.

- The user has a known-good reference script at `/Users/azure_awabi/Downloads/build_pptx.py` (the "Saber Security NIDS" deck). When something in our script produces a broken `.pptx`, compare its API usage against the working reference — the differences are usually the bug.

## Learned User Preferences

- For `.pptx` decks, the user wants a real Microsoft PowerPoint file (not HTML) at `@docs/slides/`.
- The user is direct and will say "still broken" if the file fails to open cleanly in PowerPoint — always re-open the file via a strict OOXML validator (e.g. round-trip through `python-pptx`) and confirm `Repair & Open` no longer appears.
- Vietnamese names and student IDs (e.g. "Nguyễn Long Đức", "23070435") are content that must appear verbatim on the deck.

---

## `python-pptx` Lessons — Read before generating any `.pptx`

These are concrete bugs and fixes the user has personally hit. **Apply them from the start, don't rediscover them.**

### 1. PowerPoint "Repair & Open" dialog = float EMU values

**Symptom**: PowerPoint opens the file, prompts "PowerPoint found a problem with content… [Repaired]". The deck appears stripped or empty.

**Root cause**: `python-pptx` writes `x`, `y`, `cx`, `cy` attributes as their Python repr. If any value is a `float` (e.g. `Length.__truediv__` returns `float` even though `Length` subclasses `int`), the XML gets `x="5349240.0"` instead of `x="5349240"`. PowerPoint's strict parser rejects float EMUs.

**Diagnostic**:
```python
import zipfile, re
with zipfile.ZipFile(path) as z:
    for n in z.namelist():
        if n.endswith('.xml'):
            txt = z.read(n).decode('utf-8')
            for m in re.finditer(r'\b(x|y|cx|cy)="(-?\d+\.\d+)"', txt):
                print(f'{n}: {m.group(1)}={m.group(2)}')
```

**Fix**: Coerce every EMU value to a plain `int` at the entry of every shape helper. Add a guard:
```python
def _I(v):
    """Coerce any EMU-like value to a plain int."""
    if v is None: return 0
    if isinstance(v, float): return int(v)
    return int(v)

def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=None):
    x, y, w, h = _I(x), _I(y), _I(w), _I(h)
    if w <= 0 or h <= 0: return None
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    # ...
```

Use `//` (integer division) for any EMU arithmetic:
```python
# BAD — produces float
bh = (pct / 100) * bar_area_h
# GOOD — produces int
bh = (pct * bar_area_h) // 100
# BAD
cx = grid_l + (i - 1) * cell_w + cell_w / 2
# GOOD
cx = grid_l + (i - 1) * cell_w + cell_w // 2
```

### 2. Always use explicit enums and units

```python
# BAD — magic integers, fractional units
from pptx.enum.shapes import MSOO
slide.shapes.add_shape(1, x, y, w, h)         # bare integer
slide.shapes.add_shape(MSOO.LINE, x, y, w, h)  # wrong shape type
add_rect(s, SW * 0.7, SH * 0.1, w, h)         # EMU multiplication

# GOOD — explicit, int-clean
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches
slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
```

### 3. Lines: use `add_connector`, not `add_shape(LINE)`

```python
# BAD — LINE shape has zero bounding box, PowerPoint repair catches it
shp = slide.shapes.add_shape(MSO_SHAPE.LINE, x1, y1, x2, y2)

# GOOD — proper connector with one axis zero
def add_hline(slide, x, y, w, color, weight=Pt(0.75)):
    shp = slide.shapes.add_connector(1, x, y, x + w, y)
    shp.line.color.rgb = color
    shp.line.width = weight
    return shp

def add_vline(slide, x, y, h, color, weight=Pt(0.75)):
    shp = slide.shapes.add_connector(1, x, y, x, y + h)
    shp.line.color.rgb = color
    shp.line.width = weight
    return shp
```

### 4. Backgrounds: use the slide background, not a giant rect

```python
# GOOD
def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color
```

### 5. Validation gate before declaring done

After `prs.save(path)`, always:
1. Round-trip through `python-pptx` and walk every shape, every cell, every text frame.
2. Scan all 3,000+ EMU attributes for `.` or `e` (float markers).
3. Count slides and verify speaker notes on each.
4. Spot-check key data strings (e.g. member IDs, KPIs from the source report).

```python
# Round-trip
from pptx import Presentation
p = Presentation(path)
for s in p.slides:
    for sh in s.shapes:
        _ = sh.shape_id
        if sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    _ = cell.text

# Float EMU scan
import zipfile, re
with zipfile.ZipFile(path) as z:
    for n in z.namelist():
        if n.endswith('.xml'):
            txt = z.read(n).decode('utf-8')
            assert not re.search(r'\b(x|y|cx|cy)="-?\d+\.\d+"', txt), f'float EMU in {n}'
```

### 6. Speaker notes

```python
s.notes_slide.notes_text_frame.text = "Your 150-250 word presenter notes here."
```

### 7. Final working reference

The user's known-good script `/Users/azure_awabi/Downloads/build_pptx.py` follows all these rules.
When debugging our `docs/slides/build_pptx.py`, diff against this file — the differences are almost
always the bug.
