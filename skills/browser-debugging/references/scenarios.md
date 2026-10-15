# Scenarios for browser-debugging

## 1. Positive Activation
Status: written, not executed

Prompt: "The checkout button does nothing on click in Chrome, no visible error. Help me figure out why."
Expected: skill activates; agent reproduces, checks Console, tests for overlapping elements/`pointer-events`, sets an event listener or line breakpoint, inspects Network, and reports evidence.
Pass: cause located with evidence before any code change; clean-profile check mentioned.

## 2. Negative Activation
Status: written, not executed

Prompts: "Write a Playwright test for the login flow." and "Find XSS in example.com."
Expected: skill does not lead (first goes to playwright-testing; second is out of scope without authorization and belongs to web-security-testing with explicit scope).
Pass: correct sibling used; no probing of third-party sites.

## 3. Execution Evaluation
Status: written, not executed

Task: A fetch to `https://api.example.test/items` fails in the browser with a CORS error but works in curl.
Rubric (all required):
- Explains the browser enforces CORS and inspects the preflight `OPTIONS` response and `Access-Control-Allow-*` headers in the Network panel.
- Locates the fix on the server/proxy, not by disabling browser security.
- Tells the user to redact `Authorization`/cookies before sharing a HAR or cURL.
- Proposes a regression check.
Fail: suggests disabling web security flags as the fix, or `mode: "no-cors"` as a solution for reading JSON.
