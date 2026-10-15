# Sources and provenance

Consulted (2026-10-15):
- https://react.dev/blog/2024/12/05/react-19 : Actions, useActionState, useOptimistic, use() (promises must be cached, not created in render), ref as prop, Context as provider.
- https://react.dev/learn/react-compiler : compiler purpose (automatic memoization), plugin name `babel-plugin-react-compiler`.
- https://react.dev/reference/react-compiler/directives : `"use memo"`, `"use no memo"`, `compilationMode` (annotation / infer / all).
- https://developer.chrome.com/docs/devtools/ : Performance, Network, Memory, Lighthouse panels.
- Core Web Vitals thresholds (LCP 2.5 s, INP 200 ms, CLS 0.1) from established web.dev documentation (https://web.dev/articles/vitals); not re-fetched in this session, verify current values.

Unverified in this session: the exact React Compiler release status and version, and which eslint-plugin-react-hooks version bundles compiler lint rules. The skill words these loosely and tells users to check the installed version.

Provenance: all text is original. Ideas-only consideration of vercel-labs/agent-skills: GitHub API reports `license: null` and the repository's LICENSE path returned 404, so no text was copied or adapted and its contents were not reproduced. No other external skill repositories were consulted.
