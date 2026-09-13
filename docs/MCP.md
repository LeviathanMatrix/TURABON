# Connect through MCP

## Public connection contract

- Endpoint: `https://turabon-api.leviathanmatrix.com/mcp`
- Transport: Streamable HTTP
- Tool-call authentication: `Authorization: Bearer <AGENT_API_KEY>`
- Credential scope: one TURABON Agent

MCP initialization and tool-schema discovery can be visible before authentication. Agent-specific catalog data, billing state, execution, operations, and delivery remain behind the Agent API key. The key establishes identity only; the server still enforces the Agent's current grants, policy, budget, billing selection, provider route, and operation evidence.

## Codex

Set the key in the environment that starts Codex:

```bash
export TURABON_AGENT_API_KEY='<your-agent-api-key>'
codex mcp add turabon \
  --url https://turabon-api.leviathanmatrix.com/mcp \
  --bearer-token-env-var TURABON_AGENT_API_KEY
codex mcp get turabon --json
```

Or merge [the TOML example](../examples/codex/config.toml.example) into `~/.codex/config.toml`, then restart Codex.

## Claude Code

Merge [the Claude Code example](../examples/claude-code/.mcp.json.example) into a local or user-level configuration. The example uses environment-variable expansion so the key is not stored in the file.

Verify with:

```text
/mcp
```

Do not commit a project-scoped `.mcp.json` containing a literal key.

## Cursor

Merge [the Cursor example](../examples/cursor/mcp.json.example) into your user-level `~/.cursor/mcp.json`. Replace the placeholder only on your local machine, then open **Cursor Settings → MCP** and verify that TURABON is enabled and tools are discovered.

## VS Code

Merge [the VS Code example](../examples/vscode/mcp.json.example) into `.vscode/mcp.json` or the user MCP configuration. VS Code prompts for the key as a masked input rather than storing it in the example file.

Use **MCP: List Servers** to start TURABON and inspect its status.

## Gemini CLI

Merge [the Gemini CLI example](../examples/gemini-cli/settings.json.example) into `~/.gemini/settings.json`, set `TURABON_AGENT_API_KEY`, restart Gemini CLI, then use:

```text
/mcp list
```

## Correct execution flow

1. Discover live tools and the current catalog.
2. Read entitlement or billing state.
3. Review the exact capability, offer, price, arguments, and route.
4. Use one stable idempotency key for one intended operation.
5. Poll the returned operation ID until terminal.
6. Retrieve delivery only after receipt-backed evidence is available.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Authentication failed | Missing, invalid, revoked, or wrong Agent key | Check the local environment variable or rotate the key in Runtime access |
| Empty catalog | Agent inactive or no current capability grant | Review the Agent and grants in TURABON |
| Policy blocked | Budget, threshold, grant, vendor, or route constraint failed | Review the returned reason and update authority in the console |
| Operation still processing | Provider or receipt verification is not terminal | Poll the original operation; do not create a replacement |
| Rate limited | Agent runtime quota reached | Wait for the returned retry interval |

## Not supported

- Browser session cookies as Agent authentication
- Provider, OpenAI, Anthropic, Google, Stripe, or wallet credentials in place of the Agent API key
- Direct access to provider secrets or payment credentials
- Public use of the testing-only `/mcp-connect` profile
