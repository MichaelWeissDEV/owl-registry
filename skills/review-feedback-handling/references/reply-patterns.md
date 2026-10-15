# Reply patterns

Short, factual, specific. Adapt tone to the project; keep claims verifiable.

## Fixed

> Fixed in `<sha>`: <what changed>. Added `<test name>` covering <case>. `<command>` now passes (<counts>).

## Fixed differently

> Took a different approach in `<sha>`: <approach>. Reason: <constraint, e.g. the suggested version breaks <caller>>. Happy to adjust if you prefer <alternative>.

## Could not reproduce

> I tried <exact input/steps> on <commit>, expecting <claim>, and got <observed>. Could you share the input or environment where it fails?

## Respectful decline

> I left this as is: <evidence: link to code, spec section, or test>. Changing it would <consequence>. Let me know if I am missing a case.

## Question that needs an answer

> Two comments pull in opposite directions: <A> vs <B>. Which should this PR follow?

## Out of scope

> Agreed this is worth doing, but it touches <area> beyond this PR. Proposed follow-up: <issue title>. I did not include it here to keep the diff reviewable.

## Clarification request

> Do you mean <interpretation 1> or <interpretation 2>? The current behavior is <observation>.

## Things to avoid in replies

- Praise filler in place of information.
- "Done" with no commit reference or evidence.
- Quoting secrets, tokens, or private logs.
- Arguing about taste when a formatter or documented rule decides.
