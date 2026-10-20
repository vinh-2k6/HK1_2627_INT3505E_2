import base64
from flask import Blueprint, request, jsonify
from models import db, Book, Category, Author

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['GET'])
def list_books():
    strategy = request.args.get('strategy', 'offset')
    limit = request.args.get('limit', default=10, type=int)
    genre_slug = request.args.get('genre', default=None, type=str)
    sort_param = request.args.get('sort', default=None, type=str)

    query = Book.query

    # 1. Filter theo genre (dựa trên Category slug)
    if genre_slug:
        query = query.join(Category).filter(Category.slug == genre_slug)

    # 2. Sort multi-key (ví dụ: ?sort=price_vnd,-title hoặc ?sort=-price_vnd)
    if sort_param:
        sort_fields = sort_param.split(',')
        for field in sort_fields:
            field = field.strip()
            if field.startswith('-'):
                col_name = field[1:]
                if hasattr(Book, col_name):
                    query = query.order_by(getattr(Book, col_name).desc())
            else:
                if hasattr(Book, field):
                    query = query.order_by(getattr(Book, field).asc())
    else:
        query = query.order_by(Book.id.asc())

    # 3. Phân trang theo Strategy
    if strategy == 'offset':
        page = request.args.get('page', default=1, type=int)
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        return jsonify({
            'strategy': 'offset',
            'data': [b.to_dict() for b in pagination.items],
            'total': pagination.total,
            'page': page,
            'pages': pagination.pages,
            'limit': limit
        })

    elif strategy == 'cursor':
        cursor = request.args.get('cursor', default=None, type=str)
        if cursor:
            try:
                # Giải mã cursor đơn giản (base64 encoded id)
                last_id = int(base64.b64decode(cursor.encode()).decode())
                query = query.filter(Book.id > last_id)
            except Exception:
                return jsonify({'error': 'Invalid cursor format'}), 400

        items = query.limit(limit + 1).all()
        has_next = len(items) > limit
        data = items[:limit]

        next_cursor = None
        if has_next and data:
            last_item_id = str(data[-1].id)
            next_cursor = base64.b64encode(last_item_id.encode()).decode()

        return jsonify({
            'strategy': 'cursor',
            'data': [b.to_dict() for b in data],
            'next_cursor': next_cursor,
            'has_next': has_next,
            'limit': limit
        })

    return jsonify({'error': 'Invalid strategy. Use offset or cursor.'}), 400

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    new_book = Book(
        title=data['title'],
        isbn=data['isbn'],
        price_vnd=data['price_vnd'],
        stock=data.get('stock', 0),
        category_id=data['category_id']
    )
    if 'author_ids' in data:
        authors = Author.query.filter(Author.id.in_(data['author_ids'])).all()
        new_book.authors.extend(authors)

    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': f'Book {book_id} deleted successfully'}), 200