# Troubleshooting MCP Servers

Work from the transport inward. Change one thing at a time and keep the failing request as evidence.

| Symptom | Likely cause | How to confirm | Fix |
| :--- | :--- | :--- | :--- |
| Client says server "failed to start" / immediate disconnect (stdio) | Server crashed on startup; wrong command or path; missing env var | Run the exact command in a terminal; read stderr | Fix the command; use absolute paths; pass required env explicitly in client config |
| Client connects then JSON parse errors | Something wrote to stdout (log line, banner, `print`) | Run the server and pipe stdout to a file; any non-JSON line is the culprit | Move all logging to stderr; silence library banners |
| Works in Inspector, fails in client | Different working directory, PATH, or Node/Python version in the client's environment | Log `process.cwd()` and versions to stderr at startup | Use absolute paths and a pinned runtime |
| Tool not listed | Registered after `connect`, schema failed to build, or client cached an old list | Call `tools/list` in the Inspector | Register before connecting; check startup stderr; restart the client |
| Model calls tool with wrong arguments | Vague description or schema without descriptions/enums | Read the tool description as the model would | Describe purpose, side effects, units, and constraints; use enums |
| `isError` results look empty | Error message not placed in a content block | Inspect raw result | Return `{content:[{type:"text",text}], isError:true}` |
| HTTP 403 from your own remote server | Origin validation rejecting a legitimate browser client | Log the received Origin | Add the exact origin to the allow-list; never use `*` with credentials |
| HTTP 400 `HeaderMismatch` / unsupported protocol version | Client and server on different revisions or a proxy rewriting headers | Compare `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name` with the body; inspect the 400 body for `supported` versions | Align revisions; make the proxy forward headers unchanged |
| SSE events arrive in bursts behind a proxy | Proxy buffering | Compare direct vs proxied behavior | Send `X-Accel-Buffering: no`; disable proxy buffering for the endpoint |
| Requests hang | Handler awaits something that never resolves; no timeout | Add a timeout and log entry/exit with request id | Per-call timeouts and cancellation handling |
| Old client cannot connect to a new server | Server implements only the stateless revision | Look for GET/`initialize` traffic in access logs | Enable SDK compatibility mode or serve the older shape |
| Path tool reads outside base directory | Containment check bypassed by `..`, absolute path, or symlink | Test with `../`, absolute, and symlink inputs | `realpath` both sides and compare with `path.relative` |

## Evidence to collect before asking for help

Server and SDK versions, spec revision, transport, the exact client config (secrets removed), stderr output from startup, and the raw failing request/response from the Inspector.

## Never

- Paste tokens or full environment dumps into logs or issues.
- Disable Origin or authentication checks "just to test" on a network-reachable server.
