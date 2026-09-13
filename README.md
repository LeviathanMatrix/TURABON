# TURABON

Connect AI agents to TURABON through a hosted Model Context Protocol (MCP) endpoint or the Agent Commerce HTTP API.

TURABON is an execution-authority layer for agent actions. A connection does **not** bypass the Agent's existing capability grants, policy, budget, payment route, idempotency checks, delivery verification, or receipt/audit trail.

## Endpoints

| Interface | URL | Authentication |
| --- | --- | --- |
| MCP (Streamable HTTP) | `https://turabon-api.leviathanmatrix.com/mcp` | Agent API key as a Bearer token |
| Agent Commerce API | `https://turabon-api.leviathanmatrix.com` | Agent API key as a Bearer token |
| TURABON console | `https://turabon.leviathanmatrix.com` | User login |

> Private MCP OAuth at `/mcp-connect` is not generally available yet. Use the public `/mcp` endpoint with an Agent API key.

## Before you connect

1. Sign in to the [TURABON console](https://turabon.leviathanmatrix.com).
2. Create or select an active Agent.
3. Review its capability grants, policy, budget, and billing route.
4. Issue an Agent API key from **Runtime access** and copy it when shown. The full key is not displayed again.
5. Store the key locally as `TURABON_AGENT_API_KEY`. Never commit it.

```bash
export TURABON_AGENT_API_KEY='<your-agent-api-key>'
```

## Fastest MCP setup

### Codex

```bash
codex mcp add turabon \
  --url https://turabon-api.leviathanmatrix.com/mcp \
  --bearer-token-env-var TURABON_AGENT_API_KEY

codex mcp get turabon --json
```

Configuration-file and other client examples:

- [Codex](examples/codex/config.toml.example)
- [Claude Code](examples/claude-code/.mcp.json.example)
- [Cursor](examples/cursor/mcp.json.example)
- [VS Code](examples/vscode/mcp.json.example)
- [Gemini CLI](examples/gemini-cli/settings.json.example)
- [Full MCP guide](docs/MCP.md)

## Fastest API check

The following calls are read-only:

```bash
curl --fail-with-body \
  -H "Authorization: Bearer ${TURABON_AGENT_API_KEY}" \
  -H 'Accept: application/json' \
  https://turabon-api.leviathanmatrix.com/api/agent-commerce/billing

curl --fail-with-body \
  -H "Authorization: Bearer ${TURABON_AGENT_API_KEY}" \
  -H 'Accept: application/json' \
  'https://turabon-api.leviathanmatrix.com/api/agent-commerce/catalog?limit=20'
```

See [Agent Commerce API](docs/API.md) before making a paid call. The Python and JavaScript examples perform read-only commands by default:

```bash
python3 examples/python/client.py catalog
node examples/javascript/client.mjs catalog
```

## MCP tools

The public endpoint advertises its supported tool schemas so compatible clients can discover the server. Reading Agent-specific catalog or billing data and executing any tool requires a current Agent API key; every call is then limited by that Agent's authority. The profile currently includes:

- `glassbox.catalog.search`
- `glassbox.billing.get_options`
- `glassbox.billing.get_credit_balance`
- `glassbox.billing.list_credit_packs`
- `glassbox.billing.purchase_credit_pack`
- `glassbox.data.call`
- `glassbox.operations.get`
- `glassbox.deliveries.get`

The `glassbox.*` prefix is a stable internal protocol name retained for compatibility; the product and public service are TURABON.

## Safety rules

- Never put an Agent API key in source code, a project repository, chat, screenshots, issue reports, or command output.
- Use the same idempotency key only when retrying the exact same request body.
- HTTP `202` means the operation was durably accepted and is still processing. Poll the returned operation; do not create a replacement payment.
- Use only capability IDs, offer IDs, and argument schemas returned by the live catalog for that Agent.
- A verified no-result response can still be a successfully delivered paid call.
- Revoke or rotate a key immediately if it is exposed.

## Repository boundary

This repository contains public connection documentation and minimal client examples only. It does not contain the TURABON service, authority engine, payment implementation, provider credentials, deployment configuration, or internal schemas.

Security reports: see [SECURITY.md](SECURITY.md).

## License

The documentation and example clients in this repository are available under the [MIT License](LICENSE). This license does not grant access to or rights in the hosted TURABON service or its private implementation.
