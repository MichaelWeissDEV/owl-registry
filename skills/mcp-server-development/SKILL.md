---
name: mcp-server-development
description: >
  Build, test, debug, and secure Model Context Protocol (MCP) servers providing
  tools, resources, and prompts to AI assistants. Use when developing custom MCP
  servers with the TypeScript or Python SDK, implementing tool handlers with Zod/Pydantic
  schema validation, configuring stdio and SSE transports, managing permission
  boundaries, or testing with the MCP Inspector.
compatibility: >
  Agent Skills-compatible coding agents implementing Model Context Protocol
  servers in TypeScript or Python.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "mcp, model-context-protocol, ai-agents, tools, resources, stdio, sse, zod"
  topics: "ai-agents, devtools, software-development"
---

# Model Context Protocol (MCP) Server Development

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard enabling AI models to interact securely with external tools, contextual data resources, and prompt templates. MCP servers run locally or remotely and communicate via standard JSON-RPC 2.0 messages over standard I/O (`stdio`) or Server-Sent Events (`SSE`).

Detailed specification and protocol architecture:
- [MCP Architecture & Protocol Guide](references/mcp-spec-guide.md)

---

## Core Rules

1. **Strict Input Schema Validation**: Every tool MUST define an explicit JSON Schema or Zod/Pydantic model for its arguments. Never accept unvalidated raw arguments.
2. **Never log to `stdout` in `stdio` mode**: Standard output is reserved strictly for JSON-RPC protocol frames. Any logging (debug prints, stack traces) must go exclusively to `stderr`.
3. **Respect Permission Boundaries**: Tools should perform only their declared action. Do not allow path traversal beyond configured working directories.
4. **Distinguish MCP Primitives**:
   - **Tools**: Model-controlled functions that execute actions or mutations (computations, API calls).
   - **Resources**: Application-controlled data sources that provide read-only context (files, logs, database schemas).
   - **Prompts**: User-controlled pre-written interaction templates.
5. **Handle errors gracefully via `isError: true`**: When a tool execution fails, return a formatted error content block rather than crashing the JSON-RPC connection.

---

## 1. Canonical TypeScript MCP Server Implementation

Using the official `@modelcontextprotocol/sdk`:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// 1. Define Tool Schema with Zod
const CalculateSumSchema = z.object({
  a: z.number().describe("First number"),
  b: z.number().describe("Second number"),
});

const CALCULATE_TOOL: Tool = {
  name: "calculate_sum",
  description: "Calculate the arithmetic sum of two numbers",
  inputSchema: {
    type: "object",
    properties: {
      a: { type: "number", description: "First number" },
      b: { type: "number", description: "Second number" },
    },
    required: ["a", "b"],
  },
};

// 2. Initialize MCP Server
const server = new Server(
  {
    name: "calculator-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 3. Register Tool Discovery Handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [CALCULATE_TOOL],
  };
});

// 4. Register Tool Execution Handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "calculate_sum") {
    throw new Error(`Unknown tool: ${request.params.name}`);
  }

  // Validate arguments against Zod schema
  const parseResult = CalculateSumSchema.safeParse(request.params.arguments);
  if (!parseResult.success) {
    return {
      content: [
        {
          type: "text",
          text: `Invalid parameters: ${parseResult.error.message}`,
        },
      ],
      isError: true,
    };
  }

  const { a, b } = parseResult.data;
  const result = a + b;

  // IMPORTANT: Log diagnostic messages to stderr, NEVER stdout!
  console.error(`[DEBUG] Computed sum: ${a} + ${b} = ${result}`);

  return {
    content: [
      {
        type: "text",
        text: `Result: ${result}`,
      },
    ],
  };
});

// 5. Connect stdio transport and start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Calculator MCP Server running on stdio");
}

main().catch((err) => {
  console.error("Fatal server error:", err);
  process.exit(1);
});
```

---

## 2. Testing with the MCP Inspector

Always test server tools and resources interactively before integrating into AI assistants:

```bash
# Run the official MCP interactive inspector GUI
npx @modelcontextprotocol/inspector node build/index.js
```
The inspector allows triggering tool executions, observing request/response JSON-RPC frames, and testing validation error handling.

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `console.log("Starting server")` in `stdio` transport | Corrupts JSON-RPC wire protocol; client drops connection | Use `console.error()` for all logging |
| Unbounded path arguments (`filePath: string`) | Path traversal (attacker reads `/etc/passwd`) | Resolve against base directory: `path.resolve(BASE_DIR, p)` and verify `isInside` |
| Crashing process on tool error | Terminate entire MCP session for the user | Return `{ content: [{ type: "text", text: err.message }], isError: true }` |
| Overly broad tools (`execute_command`) | Remote code execution vulnerability | Provide constrained, high-level tools with typed parameters |

---

## 4. Verification Checklist

- [ ] All tool parameters validated with Zod or Pydantic.
- [ ] No `stdout` writes outside of the JSON-RPC transport.
- [ ] Tool errors return `isError: true` without crashing the server.
- [ ] Path arguments restricted to authorized workspace directories.
- [ ] Tested and verified using the MCP Inspector (`npx @modelcontextprotocol/inspector`).
