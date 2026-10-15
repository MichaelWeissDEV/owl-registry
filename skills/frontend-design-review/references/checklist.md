# Review checklist and CSS recipes

## Quick scan (5 minutes)

1. Squint test: does the eye land on the primary action or key content first?
2. Resize from 1280 down to 320 px: where does it first break?
3. Tab through: is focus visible and the order sensible?
4. Switch the data: empty, one item, hundreds, very long strings.
5. Toggle dark mode and 200% zoom.

## Recipes

Fluid type with bounds:
```css
:root { --step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem); }
body { font-size: var(--step-0); line-height: 1.5; }
```

Readable measure:
```css
.prose { max-inline-size: 70ch; }
```

Responsive grid without breakpoints:
```css
.grid { display: grid; gap: var(--space-4); grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); }
```

Prevent image layout shift:
```css
img { max-inline-size: 100%; block-size: auto; }
/* and set width/height attributes or aspect-ratio on the element */
```

Respect reduced motion:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

Sticky header that does not hide focused elements:
```css
html { scroll-padding-block-start: 5rem; } /* header height */
```

## Common smells and fixes

| Smell | Fix |
|---|---|
| Multiple competing primary buttons | One primary; demote others |
| Random spacing values | Use spacing tokens |
| Text over images without scrim | Add overlay or move text |
| Tiny gray captions carrying key info | Increase size/contrast or promote |
| Fixed heights | `min-block-size` or content-driven height |
| Hover-only affordances | Provide focus and touch equivalents |
| Modals for everything | Inline or progressive disclosure where possible |
