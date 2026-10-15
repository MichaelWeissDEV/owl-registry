# DevTools cheat sheet

Panels (Chrome): Elements, Console, Sources, Network, Performance, Memory, Application, Lighthouse, Recorder, Issues, Security/Privacy panels as available. Panel names and locations change between Chrome versions; use the Command Menu (Cmd/Ctrl+Shift+P) to run commands by name, and Cmd/Ctrl+P in Sources to open a file by name.

## Console utilities

| Utility | Purpose |
|---|---|
| `$0` ... `$4` | Recently selected Elements nodes |
| `$_` | Result of the last expression |
| `$(sel)` / `$$(sel)` | `querySelector` / `querySelectorAll` shortcuts |
| `copy(value)` | Copy a value to clipboard |
| `console.table(arr)` | Tabular view |
| `monitor(fn)` | Log calls to a function |
| `getEventListeners(node)` | List listeners on a node |
| `debug(fn)` | Break when the function is called |

Utilities exist only in the DevTools console, not in page code.

## Breakpoint choice

| Question | Breakpoint |
|---|---|
| Who changes this attribute/subtree? | DOM breakpoint |
| What request triggers this? | XHR/fetch breakpoint |
| What runs when I click? | Event listener breakpoint |
| Where is this error thrown? | Pause on exceptions |
| What is the value in iteration 573? | Conditional breakpoint or logpoint |

## Network triage

1. Status and redirects.
2. Request URL, method, headers, payload.
3. Response body and `Content-Type`.
4. Timing (queueing, TTFB, download).
5. Cache headers and "from disk cache"/"from service worker" labels.
6. CORS: look at the preflight (`OPTIONS`) and the `Access-Control-*` response headers.

## Launching Chrome for remote debugging (local only)

```bash
# macOS example; use a throwaway profile directory
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 --user-data-dir="$(mktemp -d)"
```

The port is unauthenticated control of the browser. Only use on a trusted machine, localhost only.

## Redaction before sharing

Remove `Authorization`, `Cookie`, `Set-Cookie`, API keys in query strings, and personal data from HAR files, cURL commands, screenshots, and storage dumps.
