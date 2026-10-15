# Transports, Versions, and Migration

Source: MCP spec revision 2026-07-28, transports and changelog pages (checked October 2026). The TypeScript and Python SDK READMEs were consulted for package names.

## stdio

- Client launches the server as a subprocess; messages are newline-delimited JSON-RPC.
- stdout is for protocol frames only. Logs go to stderr (the client may capture or ignore them).
- A server should exit when stdin closes.
- Security is the process boundary: the server runs with the launching user's rights. Do not assume a stdio server is "safe" because it is local; it can still delete the user's files.

## Streamable HTTP (current)

- One endpoint path (for example `/mcp`) that accepts POST.
- Client sends `Accept: application/json, text/event-stream` and, in revision 2026-07-28, `MCP-Protocol-Version`, `Mcp-Method`, and (for `tools/call`, `resources/read`, `prompts/get`) `Mcp-Name` headers. Servers must reject requests whose headers disagree with the body (HTTP 400, JSON-RPC code -32020 `HeaderMismatch`).
- Reply is either `application/json` or a `text/event-stream` scoped to that request; a client closing the stream cancels the request.
- Notifications POST returns 202 with no body.
- Server-initiated needs (sampling, elicitation, roots) are not separate requests in 2026-07-28; the server returns an `InputRequiredResult` and the client retries with `inputResponses`.
- Long-lived change notifications use a `subscriptions/listen` request whose response stays open.
- SSE resumption (`Last-Event-ID`) is removed; a broken stream loses the in-flight request and the client re-issues it.
- Security requirements: validate `Origin` (403 if invalid), bind local servers to 127.0.0.1, authenticate.

## Supporting older clients (2025-03-26 to 2025-11-25)

Those revisions allowed a server-assigned `Mcp-Session-Id`, a GET stream for server-initiated messages, JSON-RPC requests on SSE streams, and resumable streams. A server that implements only 2026-07-28 should answer GET/DELETE with 405, ignore `Mcp-Session-Id` and `Last-Event-ID`. A server that wants to serve both eras follows the matching revision's behavior per request. Decide explicitly; most SDKs handle this, so prefer the SDK's compatibility mode over hand-rolled branching.

## HTTP+SSE (2024-11-05), deprecated

Two endpoints: a GET that opens an SSE stream and emits an `endpoint` event, and a POST endpoint named in that event. Migration: host one Streamable HTTP endpoint; keep the old pair alive only while you still have old clients; remove it afterward. Clients detect old servers by POSTing first and, on 400/404/405 with a non-MCP error body, falling back to GET for an `endpoint` event.

## Migrating server code

| Old pattern | Replacement |
| :--- | :--- |
| `SSEServerTransport` (TS v1) or `sse` transport name (Python v1) | Streamable HTTP transport of the installed SDK |
| Per-connection state keyed by session id | Explicit server-minted handles passed as tool arguments, or external storage keyed by authenticated identity |
| `server.sampling` / `elicitation/create` called mid-tool | Multi Round-Trip Requests where the SDK supports revision 2026-07-28; otherwise keep to the older mechanism and note the revision |
| `@modelcontextprotocol/sdk` imports | `@modelcontextprotocol/server` (v2 line) after reading the SDK migration guide |
| `from mcp.server.fastmcp import FastMCP` | `from mcp.server import MCPServer` on the v2 line |
| Low-level `setRequestHandler(ListToolsRequestSchema, ...)` with hand-written JSON Schema | `registerTool` with a schema library, unless you need custom protocol behavior |

Do not migrate blindly: record the SDK version, run the existing test suite, and test with the Inspector and at least one real client before cutting over. The SDK v1 line receives bug and security fixes for a limited window after v2; check the README for the current commitment.

## Version-recording habit

Put these in the server README: spec revision targeted, SDK name and version, transports offered, auth model. Clients and reviewers need them to know what behavior to expect.
