from flask import Flask, jsonify, request, make_response
import math

app = Flask(__name__)


BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Clean Architecture", "author": "Robert C. Martin"},
    {"id": 3, "title": "Refactoring", "author": "Martin Fowler"},
    {"id": 4, "title": "1984", "author": "Orwell"},
    {"id": 5, "title": "Animal Farm", "author": "Orwell"},
    # Thêm dữ liệu mẫu tùy ý...
]

DEFAULT_SIZE, MAX_SIZE = 20, 100

@app.get("/books")
def list_books():
    
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400

    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    
    flt = BOOKS
    
    a = request.args.get("author")
    if a:
        flt = [b for b in flt if b["author"].lower() == a.lower()]
        
    q = request.args.get("q")
    if q:
        flt = [b for b in flt if q.lower() in b["title"].lower()]

    
    total = len(flt)
    start = (page - 1) * size
    end = start + size
    items = flt[start:end]
    total_pages = math.ceil(total / size) if total > 0 else 1

    
    def u(p):
        return f"/books?page={p}&size={size}"

    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(total_pages)}
    }

    if page > 1:
        links["prev"] = {"href": u(page - 1)}
    if end < total:
        links["next"] = {"href": u(page + 1)}

    
    body = {
        "data": items,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": total_pages
        },
        "_links": links
    }

    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    
    return resp

if __name__ == "__main__":
    app.run(debug=True)