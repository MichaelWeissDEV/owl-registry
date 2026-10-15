# Severity Rubric, Findings Template, and Scanner Limits

## Severity rubric

| Severity | Definition | Example |
| :--- | :--- | :--- |
| Critical | Directly causes secret theft, data exfiltration, remote code execution, or destructive action when the skill is followed as written | Instruction to send `~/.aws/credentials` to a URL; reverse shell |
| High | Causes dangerous behavior under common conditions or removes user oversight | Instruction to hide actions; unpinned remote script execution; late-bound remote instructions |
| Medium | Over-broad scope or weak safeguards that raise risk but need another condition | Trigger description capturing unrelated tasks; broad shell permissions requested |
| Low | Hygiene issues | Missing license, unpinned documentation links, minor ambiguity |
| Info | Observation for the reviewer | Unusual file layout |

Evidence standard: each finding cites file, line or quoted text, what the agent would do, and why it is harmful. If you could not confirm intent, say "suspicious, intent unconfirmed" and keep the severity based on potential impact.

## Audit write-up template

```markdown
# Skill audit: <name>
- Source: <URL>
- Pinned revision: <commit SHA or sha256 of archive>
- Date / auditor:
- Method: static, read-only; no package code executed
- Decision: Approve | Approve with restrictions | Reject

## Findings
### [SEVERITY] <short title>
- Location: <path>:<line>
- Evidence: "<quoted text, truncated; no secret values>"
- Impact:
- Recommendation:

## Not reviewed / residual risk
<files or behaviors the audit could not cover, e.g. content fetched at run time>

## Restrictions if approved
<sandbox, no credentials in environment, tool permission limits, re-audit on update>
```

## What the scanner cannot see

- Paraphrased or translated injection ("disregard what you were told earlier").
- Instructions split across files, or assembled from innocuous fragments.
- Encoded content (base64, hex, ROT13) that is decoded by the agent or a script at run time.
- Content fetched from the network when the skill runs; the audited text may be clean while the remote text is not.
- Behavior in dependencies installed by a script.
- Homoglyph substitution inside identifiers or URLs unless you compare character classes.
- Social engineering aimed at the human reviewer.

Therefore: read the files, prefer small packages, and reject packages that depend on run-time remote instructions.

## Re-audit triggers

New version or commit, changed scripts or permissions, change of maintainer or repository ownership, new network destinations, or a report of malicious behavior from anyone else. Pin the version you approved and review diffs on update.

## Handling a suspected malicious skill

Stop using it, do not execute anything from it, keep a copy of the files for the record, tell the user which credentials it could have reached if it was ever installed (so they can rotate), and report it to the host platform or repository maintainers through the official channel.
