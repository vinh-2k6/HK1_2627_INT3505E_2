import base64
import json
from flask import Flask, jsonify, request

app = Flask(__name__)


ORDERS_DB = [
    {
        "id": 1,
        "customer_id": 101,
        "status": "paid",
        "total": 150.5,
        "created_at": "2026-09-01T10:00:00Z",
    },
    {
        "id": 2,
        "customer_id": 102,
        "status": "pending",
        "total": 89.0,
        "created_at": "2026-09-02T11:30:00Z",
    },
    {
        "id": 3,
        "customer_id": 101,
        "status": "paid",
        "total": 200.0,
        "created_at": "2026-09-03T09:15:00Z",
    },
    {
        "id": 4,
        "customer_id": 103,
        "status": "cancelled",
        "total": 45.0,
        "created_at": "2026-09-04T14:20:00Z",
    },
    {
        "id": 5,
        "customer_id": 102,
        "status": "paid",
        "total": 310.0,
        "created_at": "2026-09-05T16:45:00Z",
    },
    {
        "id": 6,
        "customer_id": 101,
        "status": "paid",
        "total": 120.0,
        "created_at": "2026-09-06T08:00:00Z",
    },
    {
        "id": 7,
        "customer_id": 104,
        "status": "pending",
        "total": 95.0,
        "created_at": "2026-09-07T12:00:00Z",
    },
    {
        "id": 8,
        "customer_id": 101,
        "status": "paid",
        "total": 500.0,
        "created_at": "2026-09-08T15:30:00Z",
    },
]



def encode_cursor(data_id: int) -> str:
    return base64.b64encode(str(data_id).encode("utf-8")).decode("utf-8")


def decode_cursor(cursor_str: str) -> int:
    try:
        decoded_bytes = base64.b64decode(cursor_str.encode("utf-8"))
        return int(decoded_bytes.decode("utf-8"))
    except Exception:
        raise ValueError("Invalid cursor format")


@app.route("/orders", methods=["GET"])
def get_orders():
    # 1. Parse Query Parameters
    cursor_param = request.args.get("cursor")
    limit = request.args.get("limit", default=10, type=int)
    status_filter = request.args.get("status")
    customer_id_filter = request.args.get("customer_id", type=int)
    sort_param = request.args.get("sort", default="id")  # VD: id, -id, total
    fields_param = request.args.get("fields")  # Sparse fieldsets: id,total

    data = ORDERS_DB.copy()

    
    last_id = None
    if cursor_param:
        try:
            last_id = decode_cursor(cursor_param)
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Invalid cursor provided.",
                    }
                ),
                400,
            )

    
    if status_filter:
        data = [item for item in data if item["status"] == status_filter]

    if customer_id_filter is not None:
        data = [
            item for item in data if item["customer_id"] == customer_id_filter
        ]

    
    reverse = False
    sort_key = sort_param
    if sort_param.startswith("-"):
        reverse = True
        sort_key = sort_param[1:]

    if data and sort_key in data[0]:
        data = sorted(data, key=lambda x: x[sort_key], reverse=reverse)

    
    if last_id is not None:
        
        start_index = 0
        found = False
        for i, item in enumerate(data):
            if item["id"] == last_id:
                start_index = i + 1
                found = True
                break
        if found:
            data = data[start_index:]
        else:
            data = []

    
    paginated_data = data[:limit]

    
    next_cursor = None
    if len(data) > limit and len(paginated_data) > 0:
        last_item_id = paginated_data[-1]["id"]
        next_cursor = encode_cursor(last_item_id)

    
    if fields_param:
        requested_fields = [f.strip() for f in fields_param.split(",")]
        filtered_results = []
        for item in paginated_data:
            filtered_item = {
                k: v for k, v in item.items() if k in requested_fields
            }
            filtered_results.append(filtered_item)
        paginated_data = filtered_results

    
    return jsonify(
        {
            "data": paginated_data,
            "pagination": {
                "limit": limit,
                "next_cursor": next_cursor,
                "has_more": next_cursor is not None,
            },
        }
    )


if __name__ == "__main__":
    app.run(debug=True)