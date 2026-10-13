from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS  # <--- 1. Import thư viện CORS
import yaml
import json

app = Flask(__name__)
CORS(app)  # <--- 2. Kích hoạt CORS cho toàn bộ ứng dụng Flask

# Giả lập Database trong bộ nhớ
tasks = [
    {"id": 1, "title": "Làm bài tập Flask", "completed": False},
    {"id": 2, "title": "Soạn file openapi.yaml", "completed": True}
]

# 1. Endpoint trả về cấu hình OpenAPI dưới dạng JSON
@app.route('/openapi.json', methods=['GET'])
def get_openapi_json():
    with open('openapi.yaml', 'r', encoding='utf-8') as f:
        yaml_content = yaml.safe_load(f)
    return jsonify(yaml_content)

# 2. Endpoint giao diện Swagger UI tại /docs
@app.route('/docs', methods=['GET'])
def swagger_ui():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Swagger UI</title>
      <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
      <script>
        SwaggerUIBundle({
          url: '/openapi.json',
          dom_id: '#swagger-ui',
        });
      </script>
    </body>
    </html>
    """
    return html_code

# --- API ENDPOINTS (Logic xử lý cho 5 route) ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    task_title = data.get("title", "Task mới")
    
    new_task = {
        "id": len(tasks) + 1,
        "title": task_title,
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        data = request.get_json() or {}
        task["title"] = data.get("title", task["title"])
        task["completed"] = data.get("completed", task["completed"])
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"result": "Deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)