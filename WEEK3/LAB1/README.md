## 🏗️ 1. Thiết kế Resource & Kiến trúc API

### 📋 Danh sách Resources
| Resource | Ghi chú |
| :--- | :--- |
| **users** | Tài khoản người dùng |
| **profile** | Hồ sơ, quan hệ 1-1 với user |
| **posts** | Bài viết, quan hệ N-1 với user |
| **comments** | Bình luận, quan hệ N-1 với post |
| **tags** | Thẻ, quan hệ N-N với posts |
| **follows** | Mô hình hóa thành sub-collection following/followers |

---

### 📂 Phân loại Resources & Đường dẫn
| Loại | Đường dẫn |
| :--- | :--- |
| **Collection** | `/users`, `/posts`, `/tags` |
| **Item** | `/users/{user_id}`, `/posts/{post_id}`, `/tags/{slug}`, `/comments/{comment_id}` |
| **Singleton sub-resource** | `/users/{user_id}/profile` |
| **Sub-collection** | `/posts/{post_id}/comments`, `/posts/{post_id}/tags`, `/users/{user_id}/posts`, `/users/{user_id}/followers`, `/users/{user_id}/following` |
| **Item của sub-collection** | `/users/{user_id}/following/{target_id}` |

---

### 🌳 Sơ đồ cây Endpoint (`/api/v1`)

```text
/api/v1
├── /users
│   ├── GET, POST
│   └── /{user_id}
│       ├── GET, PATCH, DELETE
│       ├── /profile                GET, PUT
│       ├── /posts                  GET
│       ├── /followers              GET
│       └── /following              GET
│           └── /{target_id}        PUT (follow), DELETE (unfollow)
├── /posts
│   ├── GET, POST
│   └── /{post_id}
│       ├── GET, PUT, PATCH, DELETE
│       ├── /comments               GET, POST
│       └── /tags                   GET
│           └── /{slug}             PUT (attach), DELETE (detach)
├── /comments
│   └── /{comment_id}               GET, PATCH, DELETE
└── /tags
    ├── GET
    └── /{slug}
        ├── GET
        └── /posts                  GET
```

---

## 📌 2. Triển khai Mã nguồn Endpoints (`/posts`)

Dưới đây là mã nguồn Flask tương ứng với các thao tác CRUD trên tập tài nguyên `/posts`:

### 2.1. Lấy danh sách bài viết (GET `/api/v1/posts`)
- **Mô tả:** Trả về danh sách bài viết trong hệ thống, hỗ trợ lọc theo tham số `tag`.
- **Mã nguồn triển khai:**

```python
@app.route(f"{API_PREFIX}/posts", methods=["GET"])
def get_posts():
    tag = request.args.get("tag")
    if tag:
        filtered_posts = [p for p in posts_db if tag in p.get("tags", [])]
        return jsonify({"data": filtered_posts, "total": len(filtered_posts)}), 200

    return jsonify({"data": posts_db, "total": len(posts_db)}), 200
```

---

### 2.2. Tạo bài viết mới (POST `/api/v1/posts`)
- **Mô tả:** Thêm bài viết mới vào collection `/posts`.
- **Mã nguồn triển khai:**

```python
@app.route(f"{API_PREFIX}/posts", methods=["POST"])
def create_post():
    data = request.get_json() or {}

    if not data.get("title") or not data.get("content"):
        return jsonify({"error": "Thiếu thông tin title hoặc content"}), 400

    new_post = {
        "id": len(posts_db) + 1,
        "title": data.get("title"),
        "content": data.get("content"),
        "author_id": data.get("author_id"),
        "tags": data.get("tags", []),
    }
    posts_db.append(new_post)
    return jsonify({"message": "Tạo bài viết thành công", "data": new_post}), 201
```

---

### 2.3. Lấy thông tin chi tiết bài viết (GET `/api/v1/posts/<post_id>`)
- **Mô tả:** Lấy thông tin chi tiết của một bài viết cụ thể theo `post_id`.
- **Mã nguồn triển khai:**

```python
@app.route(f"{API_PREFIX}/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Không tìm thấy bài viết"}), 404
    return jsonify({"data": post}), 200
```

---

### 2.4. Cập nhật bài viết (PUT `/api/v1/posts/<post_id>`)
- **Mô tả:** Cập nhật thông tin tiêu đề, nội dung hoặc tags của bài viết.
- **Mã nguồn triển khai:**

```python
@app.route(f"{API_PREFIX}/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Không tìm thấy bài viết"}), 404

    data = request.get_json() or {}
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    post["tags"] = data.get("tags", post["tags"])

    return (
        jsonify({"message": "Cập nhật bài viết thành công", "data": post}),
        200,
    )
```

---

### 2.5. Xóa bài viết (DELETE `/api/v1/posts/<post_id>`)
- **Mô tả:** Xóa một bài viết cụ thể ra khỏi hệ thống.
- **Mã nguồn triển khai:**

```python
@app.route(f"{API_PREFIX}/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    global posts_db
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Không tìm thấy bài viết"}), 404

    posts_db = [p for p in posts_db if p["id"] != post_id]
    return jsonify({"message": "Xóa bài viết thành công"}), 200
