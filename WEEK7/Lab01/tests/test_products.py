def test_create_product_success(client):
    response = client.post(
        "/api/v1/products",
        json={
            "sku": "PROD-001",
            "name": "Mechanical Keyboard",
            "description": "RGB mechanical keyboard",
            "price_cents": 8900,
            "qty_in_stock": 25,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["sku"] == "PROD-001"
    assert data["name"] == "Mechanical Keyboard"
    assert data["price_cents"] == 8900
    assert data["qty_in_stock"] == 25
    assert data["is_archived"] is False


def test_create_product_duplicate_sku(client):
    payload = {
        "sku": "PROD-DUP",
        "name": "First Product",
        "price_cents": 1000,
        "qty_in_stock": 10,
    }
    res1 = client.post("/api/v1/products", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/products", json=payload)
    assert res2.status_code == 409


def test_get_products_list_and_pagination(client):
    for i in range(15):
        client.post(
            "/api/v1/products",
            json={
                "sku": f"PAGE-PROD-{i:03d}",
                "name": f"Product {i}",
                "price_cents": 1000 * (i + 1),
                "qty_in_stock": 5,
            },
        )

    res = client.get("/api/v1/products?page=1&size=10")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["page"] == 1


def test_get_product_detail(client):
    res = client.post(
        "/api/v1/products",
        json={
            "sku": "PROD-DETAIL",
            "name": "Detail Product",
            "price_cents": 5000,
            "qty_in_stock": 10,
        },
    )
    product_id = res.get_json()["id"]

    res_get = client.get(f"/api/v1/products/{product_id}")
    assert res_get.status_code == 200
    assert res_get.get_json()["name"] == "Detail Product"

    res_not_found = client.get("/api/v1/products/99999")
    assert res_not_found.status_code == 404


def test_patch_product(client):
    res = client.post(
        "/api/v1/products",
        json={
            "sku": "PROD-PATCH",
            "name": "Old Name",
            "price_cents": 2000,
            "qty_in_stock": 5,
        },
    )
    product_id = res.get_json()["id"]

    res_patch = client.patch(
        f"/api/v1/products/{product_id}",
        json={"name": "New Updated Name", "price_cents": 2500},
    )
    assert res_patch.status_code == 200
    updated_data = res_patch.get_json()
    assert updated_data["name"] == "New Updated Name"
    assert updated_data["price_cents"] == 2500
    assert updated_data["sku"] == "PROD-PATCH"


def test_delete_product_soft_delete(client):
    res = client.post(
        "/api/v1/products",
        json={
            "sku": "PROD-DEL",
            "name": "Delete Me",
            "price_cents": 1000,
            "qty_in_stock": 2,
        },
    )
    product_id = res.get_json()["id"]

    res_del = client.delete(f"/api/v1/products/{product_id}")
    assert res_del.status_code == 204

    # Getting deleted product should return 404
    res_get = client.get(f"/api/v1/products/{product_id}")
    assert res_get.status_code == 404


def test_reserve_product(client):
    res = client.post(
        "/api/v1/products",
        json={
            "sku": "PROD-RES",
            "name": "Reserved Product",
            "price_cents": 1500,
            "qty_in_stock": 10,
        },
    )
    product_id = res.get_json()["id"]

    # Test reserve with {"quantity": 3}
    res_reserve = client.post(
        f"/api/v1/products/{product_id}/reserve",
        json={"quantity": 3},
    )
    assert res_reserve.status_code == 200
    assert res_reserve.get_json()["qty_in_stock"] == 7

    # Test reserve with {"qty": 2}
    res_reserve2 = client.post(
        f"/api/v1/products/{product_id}/reserve",
        json={"qty": 2},
    )
    assert res_reserve2.status_code == 200
    assert res_reserve2.get_json()["qty_in_stock"] == 5

    # Test reserve out of stock (requesting 10 when 5 available)
    res_out_of_stock = client.post(
        f"/api/v1/products/{product_id}/reserve",
        json={"quantity": 10},
    )
    assert res_out_of_stock.status_code == 409
