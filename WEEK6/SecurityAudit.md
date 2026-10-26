# Báo cáo Kiểm định Bảo mật (Security Audit) - Social Network API

Tài liệu này liệt kê các điểm yếu tiềm ẩn, rủi ro lộ lọt thông tin hoặc lỗ hổng bảo mật cần khắc phục đối với các endpoint `POST /auth/login`, `POST /auth/refresh`, và `GET /posts/{id}`.

## 1. Lộ thông tin nhạy cảm qua phản hồi lỗi đăng nhập (User Enumeration)
* **Mô tả:** Nếu endpoint `POST /auth/login` trả về thông báo lỗi quá chi tiết (ví dụ: *"Tài khoản không tồn tại"* thay vì *"Tên đăng nhập hoặc mật khẩu không đúng"*), kẻ tấn công có thể lợi dụng để dò quét và thu thập danh sách các tài khoản đang tồn tại trong hệ thống.
* **Biện pháp khắc phục:** Sử dụng thông báo lỗi chung chung cho cả hai trường hợp sai tài khoản hoặc sai mật khẩu.

## 2. Thiếu cơ chế giới hạn tốc độ (Rate Limiting) trên endpoint Đăng nhập
* **Mô tả:** Endpoint `POST /auth/login` không giới hạn số lần gửi request trong một khoảng thời gian ngắn, tạo điều kiện cho kẻ tấn công thực hiện tấn công dò mật khẩu tự động (Brute-force attack hoặc Credential Stuffing).
* **Biện pháp khắc phục:** Áp dụng Rate Limiting theo IP và theo Tên đăng nhập (ví dụ: tối đa 5 lần thử sai trong 1 phút).

## 3. Quản lý vòng đời và thu hồi Refresh Token kém
* **Mô tả:** Nếu Refresh Token được lưu trữ không an toàn ở phía client (ví dụ: trong `localStorage` thay vì `HttpOnly Cookie`) hoặc hệ thống không duy trì danh sách đen (Blacklist) các token đã bị thu hồi khi người dùng đăng xuất, kẻ tấn công có thể chiếm đoạt token để duy trì quyền truy cập trái phép vĩnh viễn.
* **Biện pháp khắc phục:** Lưu Refresh Token trong `HttpOnly, Secure Cookies` và triển khai cơ chế vô hiệu hóa token khi người dùng đổi mật khẩu hoặc đăng xuất.

## 4. Lỗ hổng Broken Object Level Authorization (BOLA / IDOR) tại `GET /posts/{id}`
* **Mô tả:** Endpoint `GET /posts/{id}` chỉ kiểm tra xem người dùng đã đăng nhập hay chưa mà bỏ qua việc kiểm tra xem bài viết đó có ở trạng thái riêng tư (private) hoặc bị xóa/khóa hay không. Người dùng có thể thay đổi số ID trên URL để xem trái phép các bài viết nhạy cảm của người khác.
* **Biện pháp khắc phục:** Kiểm tra chặt chẽ quyền sở hữu hoặc quyền truy cập của người dùng hiện tại đối với tài nguyên `id` cụ thể trước khi trả về dữ liệu.

## 5. Rò rỉ thông tin qua Headers hoặc Thông báo lỗi hệ thống (Stack Trace)
* **Mô tả:** Khi xảy ra lỗi (Status Code `500`), hệ thống trả về toàn bộ thông tin chi tiết lỗi của tầng cơ sở dữ liệu hoặc framework (Stack Trace), giúp kẻ tấn công nắm được cấu trúc công nghệ nội bộ để tìm các lỗ hổng sâu hơn.
* **Biện pháp khắc phục:** Cấu hình môi trường sản xuất (Production) chỉ trả về mã lỗi chung chung và ghi log chi tiết ở phía hệ thống nội bộ.

## 6. Thiếu mã hóa dữ liệu nhạy cảm trên đường truyền (Transport Layer Security)
* **Mô tả:** Nếu hệ thống cho phép gọi API qua giao thức `HTTP` thông thường thay vì bắt buộc sử dụng `HTTPS`, mật khẩu truyền lên ở endpoint `/auth/login` và Access Token trên header có thể bị đánh cắp bằng hình thức nghe lén mạng (Man-in-the-Middle Attack).
* **Biện pháp khắc phục:** Ép buộc sử dụng HTTPS trên toàn bộ các endpoint và cấu hình HSTS (HTTP Strict Transport Security).