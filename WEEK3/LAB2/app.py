import logging
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Cấu hình logging để ghi chi tiết lỗi server-side
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Content-Type chuẩn RFC 7807
PROBLEM_JSON_MIME = "application/problem+json"



class ProblemError(Exception):
    def __init__(
        self,
        status: int,
        title: str,
        detail: str = None,
        type_: str = "about:blank",
        instance: str = None,
    ):
        super().__init__()
        self.status = status
        self.title = title
        self.detail = detail
        self.type = type_
        self.instance = instance

    def to_dict(self):
        res = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
            "instance": self.instance or request.path,
        }
        return res



def make_problem_response(data: dict, status_code: int):
    response = jsonify(data)
    response.headers["Content-Type"] = PROBLEM_JSON_MIME
    return response, status_code


@app.errorhandler(ProblemError)
def handle_problem_error(error: ProblemError):
    return make_problem_response(error.to_dict(), error.status)


@app.errorhandler(HTTPException)
def handle_http_exception(error: HTTPException):
    problem_data = {
        "type": "about:blank",
        "title": error.name,
        "status": error.code,
        "detail": error.description,
        "instance": request.path,
    }
    return make_problem_response(problem_data, error.code)


@app.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    # Log chi tiết lỗi ở server-side (không lộ stack trace ra client)
    logger.exception("Internal Server Error xảy ra: %s", str(error))

    problem_data = {
        "type": "about:blank",
        "title": "Internal Server Error",
        "status": 500,
        "detail": "An unexpected error occurred. Please try again later.",
        "instance": request.path,
    }
    return make_problem_response(problem_data, 500)



resources_db = {
    1: {"id": 1, "name": "Resource 1"},
    2: {"id": 2, "name": "Resource 2"},
}



@app.route("/resources/<int:res_id>", methods=["GET"])
def get_resource(res_id):
    if res_id not in resources_db:
        # Bắn ra ProblemError nếu không tìm thấy resource
        raise ProblemError(
            status=404,
            title="Resource Not Found",
            detail=f"Resource với ID {res_id} không tồn tại trong hệ thống.",
            type_="https://example.com/probs/resource-not-found",
        )
    return jsonify(resources_db[res_id]), 200



@app.route("/test-500", methods=["GET"])
def test_server_error():
    # Cố tình gây ra ZeroDivisionError để test handler 500
    result = 1 / 0
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)