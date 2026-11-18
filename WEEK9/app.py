from functools import wraps
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cấu hình các phiên bản
LATEST = "2"
SUPPORTED = {"1", "2", "2024-06-20"}

# Dữ liệu giả lập (USERS)
USERS = {
    1: {"f": "Văn", "l": "Nguyễn", "e": "a@vnu.vn"}
}

def api_version(supported=SUPPORTED, default=LATEST):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # 1. Lấy version từ header 'X-API-Version', nếu thiếu thì dùng giá trị default
            v = request.headers.get("X-API-Version", default)
            
            # 4. Kiểm tra nếu version không nằm trong supported thì trả về lỗi 400
            if v not in supported:
                return jsonify({"error": "unsupported version"}), 400
            
            # Gọi hàm endpoint và truyền version v vào (fn(v, *args, **kwargs))
            result = fn(v, *args, **kwargs)
            
            # Xử lý trả về response kèm header 'X-API-Version-Served'
            response = jsonify(result)
            response.headers["X-API-Version-Served"] = v
            return response
        return wrapper
    return decorator

@app.route("/users/<int:uid>")
@api_version()
def get_user(version, uid):
    u = USERS.get(uid)
    if not u:
        return {"error": "not found"}
    
    # Phân nhánh theo version trả về dữ liệu tương ứng
    if version == "1":
        return {
            "id": uid, 
            "full_name": u["f"] + " " + u["l"]
        }
    
    # Mặc định (v2 hoặc các version khác)
    return {
        "id": uid,
        "first_name": u["f"],
        "last_name": u["l"],
        "email": u["e"]
    }

if __name__ == "__main__":
    app.run(port=5000, debug=True)