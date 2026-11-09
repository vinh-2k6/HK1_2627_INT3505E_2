# Tuần 07 - Lab 01: Triển khai Backend Service với Flask, SQLAlchemy & Docker

Dự án hoàn thiện theo yêu cầu bài tập Tuần 7:
1. **Hoàn thiện Lab 1 (Product API CRUD)**:
   - `GET /api/v1/products`: Phân trang (`page`, `per_page` / `size`), loại trừ sản phẩm đã xóa mềm (`is_archived=True`).
   - `GET /api/v1/products/<int:id>`: Chi tiết sản phẩm, 404 nếu không tìm thấy hoặc đã lưu trữ.
   - `POST /api/v1/products`: Tạo mới sản phẩm, kiểm tra trùng SKU (trả 409 Conflict).
   - `POST /api/v1/products/<int:id>/reserve`: Giữ chỗ / đặt trước hàng (`quantity` hoặc `qty`), trừ `qty_in_stock`, trả 409 nếu không đủ hàng.
   - `PATCH /api/v1/products/<int:id>`: Cập nhật một phần thuộc tính sản phẩm.
   - `DELETE /api/v1/products/<int:id>`: Xóa mềm (soft-delete, đánh dấu `is_archived=True`, trả về 204 No Content).
2. **Resource OrderItem liên kết Order và Product**:
   - Tách Blueprint riêng: `/api/v1/orders`.
   - `Order` có quan hệ 1-N với `OrderItem`, mỗi `OrderItem` liên kết tới một `Product`.
   - `POST /api/v1/orders`: Tạo đơn hàng kèm danh sách sản phẩm `[{"product_id": ..., "quantity": ...}]`.
   - `GET /api/v1/orders/<int:order_id>`: Lấy chi tiết đơn hàng kèm danh sách item và thông tin sản phẩm bằng kỹ thuật **Eager Loading (`selectinload`)** để loại bỏ hoàn toàn vấn đề N+1 query.
   - `GET /api/v1/orders`: Danh sách đơn hàng có phân trang và eager loading.
3. **Đóng gói Dockerfile + docker-compose**:
   - `Dockerfile` multi-stage build (Builder + Runtime) an toàn, tối ưu dung lượng, chạy dưới user `app` không dùng root.
   - `docker-compose.yml` tích hợp sẵn service PostgreSQL 16 và API Flask (Gunicorn WSGI) có healthcheck.
4. **Health Check probes**:
   - `/healthz`: Liveness probe (nhẹ, không truy vấn database, trả về 200 OK).
   - `/ready`: Readiness probe (kiểm tra kết nối database bằng `SELECT 1`, trả về 200 khi sẵn sàng hoặc 503 khi mất kết nối DB).
5. **Kiểm thử tự động với Pytest**:
   - Test đầy đủ các endpoint CRUD sản phẩm và đơn hàng.
   - Bắt sự kiện SQL query bằng SQLAlchemy event listener để kiểm tra số truy vấn khi GET đơn hàng có nhiều sản phẩm (`len(queries) <= 3`), chứng minh đã giải quyết bẫy N+1 query.

---

## 1. Cấu trúc thư mục

```text
Lab01/
├── Dockerfile                  # Multi-stage Dockerfile cho production
├── docker-compose.yml          # Compose file quản lý Flask API và PostgreSQL
├── entrypoint.sh               # Entrypoint script tự động migration và khởi động Gunicorn
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── wsgi.py                     # Entry point cho WSGI server (Gunicorn)
├── migrations/                 # Thư mục migration quản lý bởi Flask-Migrate (Alembic)
├── src/
│   ├── config.py               # Cấu hình 12-factor qua biến môi trường
│   ├── extensions.py           # Khởi tạo db, migrate, api
│   ├── main.py                 # Application factory create_app() & health check routes
│   ├── api/
│   │   ├── products.py         # Blueprint /api/v1/products
│   │   └── orders.py           # Blueprint /api/v1/orders
│   ├── models/
│   │   ├── products.py         # Model Product
│   │   ├── orders.py           # Model Order
│   │   └── orders_item.py      # Model OrderItem liên kết Order và Product
│   └── schemas/
│       ├── products.py         # Marshmallow schema cho Product
│       └── orders.py           # Marshmallow schema cho Order và OrderItem
└── tests/
    ├── conftest.py             # Fixture khởi tạo SQLite in-memory cho test suite
    ├── test_health.py          # Test cho /healthz và /ready
    ├── test_products.py        # Test các endpoint Product
    └── test_orders.py          # Test POST đơn hàng và GET có eager loading chống N+1
```

---

## 2. Hướng dẫn chạy với Docker Compose

Chạy lệnh sau tại thư mục `Lab01`:

```bash
docker compose up --build
```

- Hệ thống sẽ tự động khởi chạy PostgreSQL 16, đợi database sẵn sàng (`service_healthy`).
- Container `api` sẽ tự động thực thi database migration (`flask db upgrade`) và khởi động Gunicorn server trên port `5000`.
- Truy cập Swagger UI tại: [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui)
- Kiểm tra Liveness: [http://localhost:5000/healthz](http://localhost:5000/healthz)
- Kiểm tra Readiness: [http://localhost:5000/ready](http://localhost:5000/ready)

---

## 3. Hướng dẫn chạy và test cục bộ (Local)

### Cài đặt môi trường

```bash
pip install -r requirements.txt
```

### Chạy kiểm thử tự động (Pytest)

```bash
pytest tests -v
```

Kết quả: Toàn bộ 13/13 test cases đều PASSED, bao gồm test phát hiện và chống N+1 query.
