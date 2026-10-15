# Model Context Protocol (MCP) Architecture & Transports

## 1. Protocol Architecture & Transports

MCP is based on JSON-RPC 2.0 messages. It currently defines two primary transports:

### Standard Input/Output (`stdio`)
- Best for local subprocesses launched directly by desktop applications (Claude Desktop, Cursor, local agent CLI).
- Fast, zero-network overhead, authenticated by local process isolation.
- **Rule**: Client writes JSON-RPC requests to the server's `stdin`; server writes responses to `stdout`. Any non-JSON output on `stdout` breaks the JSON parser!

### Server-Sent Events (`SSE`)
- Best for remote servers, multi-tenant deployments, or cloud infrastructure.
- Uses HTTP POST for client-to-server messages and HTTP SSE streams for server-to-client notifications.

---

## 2. MCP Core Primitives

- **Tools (`tools/list`, `tools/call`)**: Actions that allow the model to manipulate external systems or perform computations.
- **Resources (`resources/list`, `resources/read`)**: Read-only contextual data providers (similar to GET endpoints) with URI schemas (`file:///...`, `postgres://...`).
- **Prompts (`prompts/list`, `prompts/get`)**: Reusable prompt templates with argument interpolation exposed to the user UI.
