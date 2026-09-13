# Agent Commerce API

## Contract

- Base URL: `https://turabon-api.leviathanmatrix.com`
- Authentication: `Authorization: Bearer <AGENT_API_KEY>`
- Request and response type: JSON

Export the key locally:

```bash
export TURABON_AGENT_API_KEY='<your-agent-api-key>'
```

## Recommended flow

| Step | Endpoint | Purpose |
| --- | --- | --- |
| 1 | `GET /api/agent-commerce/billing` | Read the Agent's current billing mode and route |
| 2 | `GET /api/agent-commerce/catalog` | Read granted capabilities, offers, prices, and argument schemas |
| 3 | `POST /api/agent-commerce/data-calls` | Submit one governed data call |
| 4 | `GET /api/agent-commerce/operations/{operationId}` | Poll the original durable operation |
| 5 | `GET /api/agent-commerce/operations/{operationId}/delivery` | Retrieve verified delivery |
| 6 | `GET /api/agent-commerce/purchases` | Review recent purchases and delivery state |

## Read-only requests

```bash
curl --fail-with-body \
  -H "Authorization: Bearer ${TURABON_AGENT_API_KEY}" \
  -H 'Accept: application/json' \
  https://turabon-api.leviathanmatrix.com/api/agent-commerce/billing
```

```bash
curl --fail-with-body \
  -H "Authorization: Bearer ${TURABON_AGENT_API_KEY}" \
  -H 'Accept: application/json' \
  'https://turabon-api.leviathanmatrix.com/api/agent-commerce/catalog?query=geocoding&limit=20'
```

## Submit one governed call

This request can cause a charge or consume API Credits. Copy `capabilityId`, `offerId`, and the allowed `toolArguments` schema from the live catalog. Do not invent them.

```bash
IDEMPOTENCY_KEY="turabon-example-$(date +%s)"

curl --fail-with-body \
  -X POST \
  -H "Authorization: Bearer ${TURABON_AGENT_API_KEY}" \
  -H "Idempotency-Key: ${IDEMPOTENCY_KEY}" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  https://turabon-api.leviathanmatrix.com/api/agent-commerce/data-calls \
  --data '{
    "capabilityId": "<CAPABILITY_ID_FROM_CATALOG>",
    "offerId": "<OFFER_ID_FROM_CATALOG>",
    "toolArguments": {}
  }'
```

Use one new key for one intentionally new call. Reuse a key only for the exact same body. If the response is `202`, follow the returned status URL or operation ID and do not submit a second payment.

## Common failures

| HTTP / code | Meaning | Correct response |
| --- | --- | --- |
| `400 MALFORMED_BACKEND_PAYLOAD` | Missing, unknown, or invalid fields | Re-read the live catalog schema |
| `401 UNAUTHORIZED` | Agent key is missing, invalid, or revoked | Issue or rotate the Agent key |
| `403 POLICY_BLOCKED` | Current authority does not allow the action | Review grants, budget, policy, and route |
| `409` conflict | Version, lifecycle, or idempotency conflict | Refresh state; do not change a retry body |
| `425` processing/not ready | Existing operation or route is not terminal | Poll/reconcile the original operation |
| `429` rate limit | Runtime quota reached | Respect the retry interval |
| `503` unavailable | A required trusted dependency is unavailable | Stop and retry after service recovery |

## What the API never accepts as authority

- Browser cookies for Agent runtime calls
- Caller-selected provider secrets or Stripe account IDs
- Agent self-report as proof of payment, delivery, or success
- A changed amount, offer, target, or payload under an old approval/idempotency binding
