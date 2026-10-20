# Bookstore API — Flask Pagination

## 1. Giới thiệu
Project triển khai API quản lý danh sách sách bằng Flask và Flask-SQLAlchemy, tập trung vào các chức năng:
- Offset pagination.
- Cursor pagination.
- Lọc sách theo thể loại (genre).
- Sắp xếp theo nhiều trường (multi-key sort).
- Kiểm thử tự động bằng pytest.

## 2. Công nghệ sử dụng
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- pytest

## 3. API danh sách sách
Endpoint:
`GET /api/v1/books`

### Offset pagination
`GET /api/v1/books?strategy=offset&limit=10&offset=0`
- `limit`: số sách tối đa mỗi trang.
- `offset`: số bản ghi bỏ qua trước khi lấy trang.
- `strategy`: chọn chiến lược phân trang.

### Cursor pagination
`GET /api/v1/books?strategy=cursor&limit=10`
Dùng giá trị `next_cursor` trong response để lấy trang tiếp theo:
`GET /api/v1/books?strategy=cursor&limit=10&cursor=10`

### Lọc theo thể loại
`GET /api/v1/books?genre=Fantasy`

### Sắp xếp nhiều trường
`GET /api/v1/books?sort=genre,-title`
Dấu `-` trước tên trường biểu thị thứ tự giảm dần. Ví dụ trên sắp xếp genre tăng dần và title giảm dần.

### Kết hợp các tham số
`GET /api/v1/books?strategy=offset&genre=Fantasy&sort=-published_year,title&limit=5&offset=0`

## 4. Postman collection
File collection được lưu tại:
`postman/bookstore-api.postman_collection.json`

Dưới đây là hình ảnh cấu trúc và các request trong Postman Collection:

- **Tổng quan Postman Collection & List Books (Default):**
  ![Postman Collection Overview](./images/image_d616df.jpg)

- **List Books (Offset Pagination):**
  ![List Books (Offset Pagination)](./images/image_d612de.jpg)

- **List Books (Cursor Pagination):**
  ![List Books (Cursor Pagination)](./images/image_d61300.jpg)

- **List Books (Cursor & Limit):**
  ![List Books (Cursor & Limit)](./images/image_d6131c.jpg)

- **List Books (Filter & Multi-sort):**
  ![List Books (Filter & Multi-sort)](./images/image_d61339.jpg)

- **Create New Book:**
  ![Create New Book](./images/image_d6133f.jpg)
