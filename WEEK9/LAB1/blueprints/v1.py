from flask import Blueprint
from .users_data import get_user

bp = Blueprint("v1", __name__)

@bp.after_request
def add_deprecation_headers(response):
    # Gắn Sunset header theo chuẩn RFC 8594 khi v1 sắp tắt
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Wed, 31 Dec 2026 23:59:59 GMT"
    response.headers["Link"] = '</api/v2/users>; rel="successor-version"'
    return response

@bp.route("/users/<int:uid>", methods=["GET"])
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {
        "id": uid,
        "full_name": f"{u['first_name']} {u['last_name']}",
        "email": u["email"],
    }