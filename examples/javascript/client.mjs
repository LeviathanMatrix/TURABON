#!/usr/bin/env node

const baseUrl = (process.env.TURABON_API_BASE_URL || "https://turabon-api.leviathanmatrix.com").replace(/\/$/, "");
const apiKey = (process.env.TURABON_AGENT_API_KEY || "").trim();

if (!apiKey) {
  console.error("Set TURABON_AGENT_API_KEY before running this example.");
  process.exit(1);
}

const [command, ...args] = process.argv.slice(2);

async function request(method, path, { body, idempotencyKey } = {}) {
  const headers = { Accept: "application/json", Authorization: `Bearer ${apiKey}` };
  if (body) headers["Content-Type"] = "application/json";
  if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;
  const response = await fetch(`${baseUrl}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await response.text();
  let payload;
  try { payload = text ? JSON.parse(text) : {}; }
  catch { payload = { raw: text }; }
  if (!response.ok) throw new Error(`TURABON returned HTTP ${response.status}: ${JSON.stringify(payload)}`);
  return payload;
}

let result;
if (command === "billing") {
  result = await request("GET", "/api/agent-commerce/billing");
} else if (command === "catalog") {
  const query = new URLSearchParams({ query: args[0] || "", limit: "20" });
  result = await request("GET", `/api/agent-commerce/catalog?${query}`);
} else if (command === "operation" && args[0]) {
  result = await request("GET", `/api/agent-commerce/operations/${encodeURIComponent(args[0])}`);
} else if (command === "delivery" && args[0]) {
  result = await request("GET", `/api/agent-commerce/operations/${encodeURIComponent(args[0])}/delivery`);
} else if (command === "call" && args.length >= 3) {
  const toolArguments = JSON.parse(args[2]);
  if (!toolArguments || Array.isArray(toolArguments) || typeof toolArguments !== "object") {
    throw new Error("tool arguments must be a JSON object");
  }
  result = await request("POST", "/api/agent-commerce/data-calls", {
    body: { capabilityId: args[0], offerId: args[1], toolArguments },
    idempotencyKey: `turabon-js-${crypto.randomUUID()}`,
  });
} else {
  console.error("Usage: client.mjs billing | catalog [query] | operation ID | delivery ID | call CAPABILITY OFFER '{...}'");
  console.error("Warning: call can spend money or API Credits.");
  process.exit(2);
}

console.log(JSON.stringify(result, null, 2));
