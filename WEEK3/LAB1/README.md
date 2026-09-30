### 1. Lấy danh sách bài viết (GET `/api/v1/posts`)
- **Mô tả:** Trả về danh sách tất cả bài viết hoặc lọc bài viết theo tham số `tag`.
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

### 2. Tạo bài viết mới (POST `/api/v1/posts`)
- **Mô tả:** Nhận dữ liệu JSON gồm `title`, `content`, `author_id`, `tags` để thêm bài viết mới vào hệ thống.
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

### 3. Lấy thông tin chi tiết bài viết (GET `/api/v1/posts/<post_id>`)
- **Mô tả:** Tìm và trả về chi tiết 1 bài viết dựa theo `post_id`.
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

### 4. Cập nhật bài viết (PUT `/api/v1/posts/<post_id>`)
- **Mô tả:** Cập nhật thông tin bài viết (`title`, `content`, `tags`) dựa theo `post_id`.
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

### 5. Xóa bài viết (DELETE `/api/v1/posts/<post_id>`)
- **Mô tả:** Xóa một bài viết ra khỏi cơ sở dữ liệu dựa theo `post_id`.
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
