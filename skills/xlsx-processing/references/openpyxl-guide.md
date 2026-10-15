# openpyxl Patterns, Formulas & Formatting Guide

## 1. Common Number Formats

| Format String | Description | Example Display |
| :--- | :--- | :--- |
| `#,##0` | Integer with thousands separator | `1,250` |
| `#,##0.00` | Decimal with 2 places | `1,250.75` |
| `$#,##0.00` | Currency (USD) | `$1,250.75` |
| `[$€-2] #,##0.00` | Currency (EUR) | `€ 1,250.75` |
| `0.0%` | Percentage with 1 decimal | `42.5%` |
| `YYYY-MM-DD` | ISO 8601 Date | `2026-10-15` |
| `hh:mm:ss` | 24-hour Time | `14:30:00` |

---

## 2. Dynamic Cell Merging & Unmerging

```python
# Merge a rectangular block of cells
ws.merge_cells("A1:E1")

# Top-left cell holds the merged value
ws["A1"] = "Consolidated Report"

# Unmerge
ws.unmerge_cells("A1:E1")
```

---

## 3. Adding Native Excel Charts

```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Departmental Budget vs Actual"
chart.y_axis.title = "Amount ($)"
chart.x_axis.title = "Department"

data_ref = Reference(ws, min_col=2, min_row=4, max_col=3, max_row=8)
cats_ref = Reference(ws, min_col=1, min_row=5, max_row=8)

chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)

ws.add_chart(chart, "G4")
```
