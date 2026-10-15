# Statistics for LLM evaluation

## Single pass rate
For n independent items with observed rate p, the normal approximation half-width of a 95% interval is 1.96 * sqrt(p(1-p)/n). It is poor near 0 or 1 or for small n; use a Wilson interval then. Items from the same source document or user are not independent: cluster them (resample clusters).

| n | half-width at p=0.8 |
|---|---|
| 50 | about 11 points |
| 100 | about 8 |
| 400 | about 4 |
| 1600 | about 2 |

## Comparing two systems on the same items
- Use the **paired** structure. Unpaired comparisons waste power because item difficulty varies far more than system quality.
- Binary outcomes: McNemar's test on the discordant pairs (b = A right/B wrong, c = A wrong/B right). Only discordant pairs carry information; if b + c is small, you cannot resolve a difference.
- Continuous or ordinal scores: paired bootstrap (bundled script; its `frac_resamples_b_gt_a` output is not a p-value, use the CI) or a paired permutation / sign-flip test.
- Report the effect size with its interval, not just a p-value.

## Stochastic systems
With temperature > 0, outputs vary run to run. Either use temperature 0 and state it, or run k samples per item and average within item before the paired analysis. Report run-to-run spread by repeating an identical configuration at least twice.

## Many comparisons
Evaluating many prompts/models/slices and highlighting the best inflates false positives. Pre-register the primary comparison; treat slice findings as hypotheses, or correct (for example Holm-Bonferroni).

## Judge reliability
- Agreement with humans: raw accuracy and Cohen's kappa (chance-corrected); with more than two raters use Krippendorff's alpha.
- Report the confusion matrix, since judges often over-pass or over-fail systematically.
- If the judge error is known, a small human-labelled subset on the actual comparison is more trustworthy than a bigger judge-only run.

## Contamination checks
For public benchmarks, check whether the items (or near paraphrases) appear in the model's training data when that is knowable; otherwise treat scores as upper bounds and prefer private, recent items for decisions. For your own fine-tuning data, run an n-gram or hash overlap check against the eval set (see dataset-quality).
