## 🛠️ Lab 2: Lint OpenAPI bằng Spectral

### 1. Khắc phục 3 lỗi (defects) trong `openapi.yaml`
* **Lỗi 1:** Bổ sung thiếu `operationId: getBooks` cho endpoint `GET /books`.
* **Lỗi 2:** Xóa bỏ phần khai báo body/schema thừa ở response `204` của endpoint `DELETE /books/{id}` (vì trạng thái 204 không có nội dung body phản hồi).
* **Lỗi 3:** Sửa kiểu dữ liệu của trường `year` trong model `Book` từ `string` thành `integer` cho đồng bộ với mô hình thực tế.

### 2. Custom Rule trong file `.spectral.yml`
File `.spectral.yml` được cấu hình thêm một custom rule để kiểm tra chất lượng schema:
```yaml
extends: ["spectral:oas"]
rules:
  response-200-has-properties:
    description: "Response với status 200 phải có ít nhất 1 trường (property) được định nghĩa trong schema."
    severity: warn
    given: "$.paths[*][*].responses['200'].content['application/json'].schema"
    then:
      field: properties
      function: truthy

### 3. Log Output khi chạy lệnh Lint
```powershell
spectral lint openapi.yaml --ruleset .spectral.yml
c:/Users/OS/Documents/GitHub/HK1_2627_INT3505E_2/WEEK8/LAB1/lab08-starter-main/openapi.yaml
  2:6    warning  info-contact               Info object must have "contact" object.                                   info
  12:9   warning  operation-description      Operation "description" must be present and non-empty string.            paths./health.get
  12:9   warning  operation-tags             Operation must have non-empty "tags" array.                              paths./health.get
  24:9   warning  operation-description      Operation "description" must be present and non-empty string.            paths./books.get
  24:9   warning  operation-tags             Operation must have non-empty "tags" array.                              paths./books.get
  42:22  warning  response-200-has-properties  Response với status 200 phải có ít nhất 1 trường (property) được định nghĩa trong schema.  paths./books.get.responses[200].content.application/json.schema
  45:10  warning  operation-description      Operation "description" must be present and non-empty string.            paths./books.post
  45:10  warning  operation-tags             Operation must have non-empty "tags" array.                              paths./books.post
  66:9   warning  operation-description      Operation "description" must be present and non-empty string.            paths./books/{id}.get
  66:9   warning  operation-tags             Operation must have non-empty "tags" array.                              paths./books/{id}.get
  75:9   warning  operation-description      Operation "description" must be present and non-empty string.            paths./books/{id}.put
  75:9   warning  operation-tags             Operation must have non-empty "tags" array.                              paths./books/{id}.put
  90:12  warning  operation-description      Operation "description" must be present and non-empty string.            paths./books/{id}.delete
  90:12  warning  operation-tags             Operation must have non-empty "tags" array.                              paths./books/{id}.delete

✖ 14 problems (0 errors, 14 warnings, 0 infos, 0 hints)