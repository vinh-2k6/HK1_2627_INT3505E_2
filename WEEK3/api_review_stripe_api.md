# 🔍 API Review: Stripe API

Báo cáo đánh giá API của **Stripe** dựa trên 9 tiêu chí thiết kế RESTful API chuẩn mực.

---

## 📋 Danh sách tiêu chí đánh giá

### 01. Tài nguyên là danh từ
- **Chi tiết:** Stripe sử dụng hoàn toàn danh từ số nhiều làm tài nguyên trên URL. Các hành động (actions) được thể hiện qua phương thức HTTP (GET, POST, DELETE).
- **Ví dụ:**
  - `GET /v1/customers` (Lấy danh sách khách hàng)
  - `POST /v1/customers` (Tạo mới khách hàng)
  - `POST /v1/payment_intents/{id}/confirm` (Ngoại lệ cho action phức tạp như confirm, cancel cũng được thiết kế chuẩn xác).

---

### 02. Naming nhất quán
- **Chi tiết:**
  - **Path:** Lowercase, kebab-case (hoặc snake_case chuẩn xác như `/v1/payment_intents`).
  - **Query parameters & JSON payload:** Đồng nhất sử dụng `snake_case` (ví dụ: `starting_after`, `payment_method_types`).
  - **Collections:** Luôn ở dạng số nhiều (`/v1/charges`, `/v1/invoices`, `/v1/coupons`).

---

### 03. Status code đúng nghĩa
- **Chi tiết:** Stripe trả về HTTP Status Code tiêu chuẩn để phản ánh chính xác kết quả giao dịch, **hoàn toàn KHÔNG trả về `200 OK` đi kèm lỗi trong body**.
- **Các mã thường gặp:**
  - `200 OK`: Thành công (GET, POST cập nhật).
  - `400 Bad Request`: Thiếu tham số bắt buộc hoặc định dạng sai.
  - `401 Unauthorized`: API Key không hợp lệ hoặc thiếu Bearer token.
  - `402 Payment Required`: Thẻ bị từ chối hoặc giao dịch thất bại.
  - `404 Not Found`: Tài nguyên không tồn tại.
  - `429 Too Many Requests`: Vượt quá Rate Limit.

---

### 04. Idempotency rõ ràng
- **Chi tiết:**
  - Stripe là minh chứng chuẩn mực về **Idempotency** trong ngành tài chính.
  - Hỗ trợ gửi `Idempotency-Key` header cho các request `POST` để tránh xử lý trùng lặp (ví dụ: bị trừ tiền 2 lần khi rớt mạng).
  - Các thao tác `GET`, `PUT`, `DELETE` mặc định mang tính idempotent.
  - Tài liệu (Documentation) hướng dẫn chi tiết cơ chế lưu trữ và hoãn trả kết quả cũ nếu key trùng lặp.

---

### 05. Error response có cấu trúc
- **Chi tiết:** Cấu trúc lỗi cực kỳ rõ ràng, tuân theo tư duy chuẩn hóa (tương tự RFC 7807), bao gồm các field nhất quán:
```json
{
  "error": {
    "code": "parameter_missing",
    "doc_url": "https://stripe.com/docs/error-codes/parameter-missing",
    "message": "Missing required param: charge.",
    "param": "charge",
    "type": "invalid_request_error"
  }
}
```

---

### 06. Pagination rõ ràng
- **Chi tiết:**
  - Sử dụng **Cursor-based Pagination** (dựa vào ID của object) thay vì Offset-based, giúp tăng hiệu năng với cơ sở dữ liệu lớn và tránh trùng lặp/sót dữ liệu khi danh sách thay đổi liên tục.
  - Tham số phân trang: `limit` (mặc định 10, tối đa 100), `starting_after`, `ending_before`.
  - Kết quả trả về kèm trường `has_more` (boolean) để client nhận biết còn dữ liệu hay không.

---

### 07. Filter/Sort đa dạng
- **Chi tiết:**
  - Hỗ trợ filter linh hoạt theo mốc thời gian (`created[gte]`, `created[lte]`).
  - Hỗ trợ lồng ghép filter sâu theo trạng thái (`status=succeeded`).
  - Hỗ trợ **Expand Objects** (tương tự sparse fieldsets / GraphQL) bằng query parameter `expand[]` để gom dữ liệu liên quan trong một request duy nhất, giúp giảm số lượng HTTP calls.

---

### 08. Authentication & security
- **Chi tiết:**
  - Xác thực qua HTTP Bearer Auth ở Header: `Authorization: Bearer sk_test_...`.
  - Tuyệt đối không lộ credentials qua URL query string.
  - **Rate Limit:** Có cơ chế giới hạn request rõ ràng (trả về HTTP `429` nếu vượt ngưỡng).
  - Hỗ trợ Phân quyền theo khóa (Restricted API Keys) chỉ cho phép truy cập đúng tài nguyên cần thiết.

---

### 09. Versioning + deprecation
- **Chi tiết:**
  - Định vị phiên bản chính qua URL Prefix: `/v1/...`
  - Đỉnh cao của Stripe là **Header-based API Versioning** theo ngày phát hành: `Stripe-Version: 2023-10-16`.
  - Cho phép mỗi account/developer ghim một API Version cụ thể trong Dashboard để tránh breaking changes khi nâng cấp.
  - Lộ trình Deprecation rõ ràng, gửi mail thông báo và log lại các request sử dụng version cũ.

---

