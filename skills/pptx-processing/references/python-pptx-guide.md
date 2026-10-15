# python-pptx Layouts, Shapes & Tables Guide

## 1. Metric Conversion & Dimensions
`python-pptx` provides metric helper classes:
- `Inches(1.0)`: 1 inch = 914,400 EMUs (English Metric Units)
- `Pt(12)`: 12 points (standard typographic size)
- `RGBColor(r, g, b)`: Explicit RGB color definition

### Widescreen 16:9 Standard
```python
from pptx.util import Inches

prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
```

---

## 2. Adding Geometric Callout Shapes

```python
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Add a rounded rectangle callout card
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(1.0), Inches(4.5), Inches(11.333), Inches(1.8)
)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xF6) # Light slate tint
shape.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

tf = shape.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Key Takeaway: Zero-downtime database migration complete."
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
```

---

## 3. Working with Master Slide Layouts

Standard default layout indices in `prs.slide_layouts`:
- `0`: Title Slide
- `1`: Title and Content
- `2`: Section Header
- `3`: Two Content
- `4`: Comparison
- `5`: Title Only
- `6`: Blank Slide (safest for custom coordinate layout generation)
