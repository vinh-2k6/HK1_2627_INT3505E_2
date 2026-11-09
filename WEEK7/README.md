# WEEK 07: NGUYÊN LÝ TRIỂN KHAI BACKEND SERVICE

Nội dung buổi học và bài tập tuần 7:
- **onClass/**: Các bản demo thực hành trên lớp:
  - `Code-First/`: Xây dựng API và sinh OpenAPI spec tự động với `flask-smorest` và Marshmallow Schema.
  - `Design-First/`: Thiết kế OpenAPI 3.0 YAML trước, ánh xạ endpoint bằng `connexion`.
- **Lab01/**: Dự án hoàn chỉnh giải quyết toàn bộ 5 yêu cầu bài tập tuần:
  1. Hoàn thiện Product API CRUD (6 endpoints).
  2. Thêm resource `OrderItem` liên kết `Order` và `Product` với Blueprint riêng `/api/v1/orders`.
  3. Đóng gói Dockerfile multi-stage + docker-compose chạy trên mọi môi trường.
  4. Hai endpoint `/healthz` (liveness) và `/ready` (readiness) độc lập.
  5. Bộ kiểm thử Pytest kiểm tra eager loading (`selectinload`) và đếm câu truy vấn nhằm phát hiện & ngăn chặn lỗi N+1 query.

## Hướng dẫn nhanh

### Khởi chạy Docker Compose:
```bash
docker compose up --build
```
Swagger UI: [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui)

### Chạy kiểm thử Pytest:
```bash
pytest Lab01/tests -v
```
