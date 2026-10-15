# Dataset card template

Copy, fill in, keep next to the data. Mark unknowns as "unknown" rather than omitting them.

```markdown
# <Dataset name> vX.Y

## Purpose and intended use
## Out-of-scope uses

## Sources
| Source | Collection method | Licence / terms | Consent basis | Date range |
|---|---|---|---|---|

## Structure
- Unit of one row:
- Fields (name, type, description, allowed values, missing-value convention):
- Label definition and annotation guideline (link/version):
- Annotators, agreement (metric, value, sample size):

## Processing log
| Step | Rule | Rows before | Rows after | Removed ids file |
|---|---|---|---|---|
| dedup exact | normalised sha256 | | | |
| near-dup | method, threshold | | | |
| PII filter | patterns/tool, review sample size | | | |

## Splits
- Method (random / grouped by X / temporal), seed, ratios, row counts per split
- Frozen test set: yes/no, date frozen
- Class distribution per split

## Known issues and biases
## Privacy and security notes
## Versioning
- Files and checksums / commit ids:
- Changes since previous version:
```
