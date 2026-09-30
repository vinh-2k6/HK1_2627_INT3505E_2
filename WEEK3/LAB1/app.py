from flask import Flask, jsonify, request

app = Flask(__name__)


posts_db = [
    {
        "id": 1,
        "title": "Học RESTful API với Flask",
        "content": "Tổng quan về thiết kế REST API chuẩn convention và triển khai routes trong Python Flask.",
        "author_id": 101,
        "tags": ["flask", "python", "api"],
    },
    {
        "id": 2,
        "title": "Hướng dẫn cấu hình Spring Security JWT",
        "content": "Bảo mật hệ thống Backend sử dụng JSON Web Token và HttpOnly Refresh Cookie.",
        "author_id": 102,
        "tags": ["java", "spring-boot", "security"],
    },
    {
        "id": 3,
        "title": "Phát hiện gian lận giao dịch với Machine Learning",
        "content": "Ứng dụng mô hình XGBoost và Graph Neural Networks trong phân tích rủi ro tín dụng.",
        "author_id": 101,
        "tags": ["python", "machine-learning", "data-science"],
    },
]

API_PREFIX = "/api/v1"



@app.route(f"{API_PREFIX}/posts", methods=["GET"])
def get_posts():
    tag = request.args.get("tag")
    if tag:
        filtered_posts = [p for p in posts_db if tag in p.get("tags", [])]
        return jsonify({"data": filtered_posts, "total": len(filtered_posts)}), 200

    return jsonify({"data": posts_db, "total": len(posts_db)}), 200



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



@app.route(f"{API_PREFIX}/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Không tìm thấy bài viết"}), 404
    return jsonify({"data": post}), 200



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



@app.route(f"{API_PREFIX}/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    global posts_db
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Không tìm thấy bài viết"}), 404

    posts_db = [p for p in posts_db if p["id"] != post_id]
    return jsonify({"message": "Xóa bài viết thành công"}), 200


if __name__ == "__main__":
    app.run(debug=True)