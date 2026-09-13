#!/usr/bin/env python3
"""Minimal dependency-free TURABON Agent Commerce client."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


BASE_URL = os.environ.get("TURABON_API_BASE_URL", "https://turabon-api.leviathanmatrix.com").rstrip("/")


def request(method: str, path: str, *, body: dict | None = None, idempotency_key: str | None = None) -> dict:
    key = os.environ.get("TURABON_AGENT_API_KEY", "").strip()
    if not key:
        raise SystemExit("Set TURABON_AGENT_API_KEY before running this example.")

    headers = {"Accept": "application/json", "Authorization": f"Bearer {key}"}
    payload = None
    if body is not None:
        payload = json.dumps(body, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key

    req = urllib.request.Request(f"{BASE_URL}{path}", data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        message = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"TURABON returned HTTP {error.code}: {message}") from error


def parse_object(value: str) -> dict:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("arguments must be a JSON object")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("billing", help="Read current Agent billing state")
    catalog = subparsers.add_parser("catalog", help="Read the Agent's granted catalog")
    catalog.add_argument("--query", default="")
    catalog.add_argument("--limit", type=int, default=20)

    call = subparsers.add_parser("call", help="Submit one governed call; this can spend money or Credits")
    call.add_argument("--capability", required=True)
    call.add_argument("--offer", required=True)
    call.add_argument("--arguments", type=parse_object, required=True)
    call.add_argument("--idempotency-key", default="")

    operation = subparsers.add_parser("operation", help="Read one existing operation")
    operation.add_argument("operation_id")
    delivery = subparsers.add_parser("delivery", help="Read verified delivery for one operation")
    delivery.add_argument("operation_id")

    args = parser.parse_args()
    if args.command == "billing":
        result = request("GET", "/api/agent-commerce/billing")
    elif args.command == "catalog":
        query = urllib.parse.urlencode({"query": args.query, "limit": args.limit})
        result = request("GET", f"/api/agent-commerce/catalog?{query}")
    elif args.command == "call":
        body = {"capabilityId": args.capability, "offerId": args.offer, "toolArguments": args.arguments}
        result = request(
            "POST",
            "/api/agent-commerce/data-calls",
            body=body,
            idempotency_key=args.idempotency_key or f"turabon-python-{uuid.uuid4()}",
        )
    elif args.command == "operation":
        result = request("GET", f"/api/agent-commerce/operations/{urllib.parse.quote(args.operation_id, safe='')}")
    else:
        result = request("GET", f"/api/agent-commerce/operations/{urllib.parse.quote(args.operation_id, safe='')}/delivery")

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
