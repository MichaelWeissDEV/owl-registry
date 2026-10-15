# Sources and provenance

Consulted (2026-10-15):
- https://wstg.owasp.org/stable/ : redirects to /v4.2/, so stable version is 4.2. The category list (INFO, CONF, IDNT, ATHN, ATHZ, SESS, INPV, ERRH, CRYP, BUSL, CLNT, APIT) is from established knowledge of WSTG 4.2; the fetched page was only a redirect notice, so verify against https://owasp.org/www-project-web-security-testing-guide/ .
- https://owasp.org/www-project-top-ten/ and OWASP cheat sheet series (headers, session management, authorization) : general knowledge, not re-fetched this session.
- https://www.zaproxy.org/docs/docker/baseline-scan/ : ZAP baseline scan described from memory (spider plus passive rules); exact command and image tag not re-verified this session, the skill tells users to check the ZAP docs.
- https://developer.mozilla.org/en-US/docs/Web/Security : header semantics; not re-fetched this session.

Unverified: CVSS version guidance and exact ZAP invocation. No exploit payloads, tool runs, or network requests against any target were performed in authoring this skill. The Playwright snippet is illustrative (uses fixtures `bobApi` and `aliceTaskId` that the reader must define) and was not executed.

Provenance: all text is original. vercel-labs/agent-skills was considered ideas-only; its GitHub license is null and its LICENSE path returned 404, so nothing was copied and its contents were not reproduced. trailofbits/skills was not consulted.
