from flask import Flask, jsonify, request

app = Flask(__name__)

BOOKS = [
    {"id": "b1", "t": "Lập trình Python cơ bản"},
    {"id": "b2", "t": "Flask Web Development"},
    {"id": "b3", "t": "Học Python qua ví dụ"},
    {"id": "b4", "t": "Cấu trúc dữ liệu và giải thuật"},
]


@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    # Tìm sách theo ID
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    
    if book is None:
        return jsonify({"error": "not found"}), 404
        
    return jsonify(book), 200



@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 20))
    q = request.args.get("q", "").strip().lower()

    items = [b for b in BOOKS if q in b["t"].lower()]
    
    items = items[:limit]

    return jsonify({"items": items}), 200


if __name__ == "__main__":
    app.run(debug=True)