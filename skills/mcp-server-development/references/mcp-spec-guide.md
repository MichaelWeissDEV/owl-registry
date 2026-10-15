# Model Context Protocol: Architecture, Primitives, Revisions

Checked against https://modelcontextprotocol.io/specification/latest (revision 2026-07-28) in October 2026. Specification text is authoritative; this page is a map.

## 1. Architecture

MCP uses JSON-RPC 2.0 messages encoded as UTF-8. A host application runs MCP clients; each client talks to one server. Protocol semantics are the same on every transport; a transport is only a binding for framing and delivery.

Standard transports (see [transports-and-migration.md](transports-and-migration.md) for details):

- **stdio**: newline-delimited JSON-RPC over the standard streams of a client-launched subprocess. stdout carries only protocol messages.
- **Streamable HTTP**: every client message is an HTTP POST to one MCP endpoint; the reply is a JSON object or a request-scoped SSE stream.

The old HTTP+SSE transport (2024-11-05) is deprecated and eligible for removal.

## 2. Server primitives

- **Tools** (`tools/list`, `tools/call`): model-invoked actions. Definition has `name`, `description`, `inputSchema` (JSON Schema), optional `outputSchema` and `annotations` (hints such as `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`).
- **Resources** (`resources/list`, `resources/read`, templates): application-controlled context addressed by URI. Not-found uses JSON-RPC Invalid Params (-32602) from revision 2026-07-28 (earlier -32002).
- **Prompts** (`prompts/list`, `prompts/get`): user-invoked templates with arguments.

Choose by who controls invocation: model (tool), application (resource), user (prompt).

## 3. Revision timeline (what changed, why it matters to a server author)

| Revision | Relevant changes |
| :--- | :--- |
| 2024-11-05 | First public revision: stdio and HTTP+SSE |
| 2025-03-26 | Streamable HTTP replaces HTTP+SSE; tool annotations; OAuth-based authorization |
| 2025-06-18 | Structured tool output (`outputSchema`), elicitation, resource links, `MCP-Protocol-Version` header, servers classified as OAuth resource servers |
| 2025-11-25 | Experimental tasks, URL-mode elicitation, further authorization updates |
| 2026-07-28 | Stateless: no `initialize`, no `Mcp-Session-Id`, no GET stream; per-request `_meta`; `server/discover`; `subscriptions/listen`; Multi Round-Trip Requests replace server-initiated requests; tasks moved to an extension; `Mcp-Method`/`Mcp-Name` headers; results carry `resultType`, list results carry `ttlMs`/`cacheScope`; Roots, Sampling, Logging deprecated |

Verify any single row against the changelog page of that revision before relying on it in code; SDKs lag the spec.

## 4. Error handling model

- Malformed request or unknown method: JSON-RPC error (for example -32601 method not found, -32602 invalid params).
- Tool executed but failed: a normal result with `isError: true` and a text content block, so the model can read and recover.
- Spec-reserved server error codes are -32020 to -32099 (for example `HeaderMismatch` -32020 in 2026-07-28). Codes -32000 to -32019 are implementation-defined.

## 5. Security model summary

- Servers are untrusted-input processors: arguments come from a model steered by untrusted text.
- Clients should treat server-provided descriptions and results as untrusted too; a server author should not rely on that and should keep descriptions factual.
- Streamable HTTP servers must validate Origin; local servers should bind to loopback; authenticate all connections.
- Authorization (HTTP): OAuth resource-server behavior, audience-bound tokens, no token passthrough. Dynamic Client Registration is deprecated in 2026-07-28 in favor of Client ID Metadata Documents, but remains for compatibility.
