## Hai Quyết Định Thiết Kế Khó Nhất

### 1. Tách biệt hoàn toàn tệp đặc tả (`openapi.yaml`) khỏi mã nguồn Flask
* **Bối cảnh & Thách thức**: Đảm bảo tài liệu API tuân thủ tiêu chuẩn OpenAPI 3.0 mà không làm rối mã nguồn Python bằng các annotation dài dòng.
* **Quyết định**: Tách riêng tệp cấu hình `openapi.yaml` để quản lý độc lập, kết hợp route `/openapi.json` để phân giải tệp cho giao diện Swagger UI.

### 2. Xử lý đồng bộ CORS và cấu hình Server để kiểm thử qua Web Editor
* **Bối cảnh & Thách thức**: Trình duyệt chặn các yêu cầu từ giao diện Swagger Editor trực tuyến gọi về máy chủ nội bộ (Localhost) do chính sách bảo mật CORS.
* **Quyết định**: Bổ sung khối `servers` trỏ về `http://127.0.0.1:5000` trong tệp YAML và kích hoạt thư viện `flask-cors` trong ứng dụng Flask.