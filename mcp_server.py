# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkCrm

client = OpenClawGenParkCrm()

TOOLS = [
    {
        "name": "calculate_continuous_rfm_score",
        "description": "Calculates continuous normalized RFM scores and classifies customer into segments.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days_since_last_purchase": {"type": "number"},
                "purchase_frequency": {"type": "integer"},
                "total_monetary_spend": {"type": "number"}
            },
            "required": ["days_since_last_purchase", "purchase_frequency", "total_monetary_spend"]
        }
    },
    {
        "name": "compute_clv_bg_nbd",
        "description": "Calculates Discounted Customer Lifetime Value (CLV) and expected lifespan.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "monthly_margin_usd": {"type": "number"},
                "monthly_retention_rate": {"type": "number"},
                "annual_discount_rate": {"type": "number"}
            },
            "required": ["monthly_margin_usd", "monthly_retention_rate"]
        }
    },
    {
        "name": "detect_churn_opportunity_loss",
        "description": "Ranks customer accounts by expected annual revenue loss from churn.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "accounts": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["accounts"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "calculate_continuous_rfm_score":
            res = client.calculate_continuous_rfm_score(args["days_since_last_purchase"], args["purchase_frequency"], args["total_monetary_spend"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_clv_bg_nbd":
            res = client.compute_clv_bg_nbd(args["monthly_margin_usd"], args["monthly_retention_rate"], args.get("annual_discount_rate", 0.10))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "detect_churn_opportunity_loss":
            res = client.detect_churn_opportunity_loss(args["accounts"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
