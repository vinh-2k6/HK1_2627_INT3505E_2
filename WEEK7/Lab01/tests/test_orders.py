from sqlalchemy import event
from src.extensions import db


def test_post_create_order(client):
    # 1. Create two products
    p1 = client.post(
        "/api/v1/products",
        json={
            "sku": "ORDER-P1",
            "name": "Mouse Wireless",
            "price_cents": 2500,
            "qty_in_stock": 20,
        },
    ).get_json()

    p2 = client.post(
        "/api/v1/products",
        json={
            "sku": "ORDER-P2",
            "name": "Mousepad Gaming",
            "price_cents": 1500,
            "qty_in_stock": 15,
        },
    ).get_json()

    # 2. Test POST /api/v1/orders
    order_res = client.post(
        "/api/v1/orders",
        json={
            "items": [
                {"product_id": p1["id"], "quantity": 3},
                {"product_id": p2["id"], "quantity": 2},
            ]
        },
    )

    assert order_res.status_code == 201
    order_data = order_res.get_json()
    assert order_data["status"] == "pending"
    assert len(order_data["items"]) == 2
    assert order_data["items"][0]["quantity"] == 3
    assert order_data["items"][0]["unit_price"] == 2500
    assert order_data["items"][1]["quantity"] == 2
    assert order_data["items"][1]["unit_price"] == 1500


def test_post_order_product_not_found(client):
    order_res = client.post(
        "/api/v1/orders",
        json={
            "items": [
                {"product_id": 99999, "quantity": 1},
            ]
        },
    )
    assert order_res.status_code == 404


def test_get_order_eager_loading_detect_n_plus_one(client, app):
    """
    Test GET /api/v1/orders/<order_id> with eager loading.
    Verify that loading an order with multiple items and their products
    does NOT trigger N+1 queries by intercepting SQL statements.
    """
    # Create 5 distinct products
    product_ids = []
    for i in range(5):
        res = client.post(
            "/api/v1/products",
            json={
                "sku": f"EAGER-SKU-{i:03d}",
                "name": f"Eager Product {i}",
                "price_cents": 1000 * (i + 1),
                "qty_in_stock": 50,
            },
        )
        assert res.status_code == 201
        product_ids.append(res.get_json()["id"])

    # Create an order containing items for all 5 products
    order_res = client.post(
        "/api/v1/orders",
        json={
            "items": [
                {"product_id": pid, "quantity": i + 1}
                for i, pid in enumerate(product_ids)
            ]
        },
    )
    assert order_res.status_code == 201
    order_id = order_res.get_json()["id"]

    # Intercept queries to detect N+1
    queries = []

    def capture_queries(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            queries.append(statement)

    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", capture_queries)
        try:
            response = client.get(f"/api/v1/orders/{order_id}")
        finally:
            event.remove(db.engine, "before_cursor_execute", capture_queries)

    assert response.status_code == 200
    data = response.get_json()

    assert data["id"] == order_id
    assert len(data["items"]) == 5
    for item in data["items"]:
        assert item["product"] is not None
        assert "sku" in item["product"]
        assert "name" in item["product"]

    # In eager loading with selectinload, at most 3 SELECT queries are issued:
    # 1. SELECT order
    # 2. SELECT order_items WHERE order_id IN (...)
    # 3. SELECT products WHERE product_id IN (...)
    # Without eager loading, 1 + 5 = 6 (or 11) queries would occur.
    assert len(queries) <= 3, f"Expected <= 3 queries (eager loading), but executed {len(queries)} queries (N+1 bug!)"


def test_patch_order_status(client):
    p = client.post(
        "/api/v1/products",
        json={"sku": "STATUS-P", "name": "Status Product", "price_cents": 500, "qty_in_stock": 10},
    ).get_json()

    order = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": p["id"], "quantity": 1}]},
    ).get_json()

    patch_res = client.patch(
        f"/api/v1/orders/{order['id']}",
        json={"status": "completed"},
    )
    assert patch_res.status_code == 200
    assert patch_res.get_json()["status"] == "completed"
