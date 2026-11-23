from flask import Blueprint, request
from .users_data import get_user, create_user

bp = Blueprint("v2", __name__)

@bp.route("/users/<int:uid>", methods=["GET"])
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {
        "id": uid,
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"],
    }

@bp.route("/users", methods=["POST"])
def create():
    data = request.get_json(silent=True) or {}
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not all([first_name, last_name, email]):
        return {"error": "first_name, last_name, and email are required"}, 400

    new_id, user = create_user(first_name, last_name, email)
    return {
        "id": new_id,
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }, 201