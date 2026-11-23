import uuid
from datetime import datetime, timezone

def v1_create_order(body):
    return {
        "order_id": f"ord_v1_{uuid.uuid4().hex[:6]}",
        "account_id": body.get("account_id"),
        "version": "v1",
        "status": "created"
    }

def v2_create_order(body):
    return {
        "order_id": f"ord_v2_{uuid.uuid4().hex[:6]}",
        "account_id": body.get("account_id"),
        "version": "v2",
        "status": "created",
        "created_at": datetime.now(timezone.utc).isoformat()
    }