from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Bảng trung gian Relationship Many-to-Many giữa Book và Author
book_authors = db.Table(
    'book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    
    # 1:N với Book
    books = db.relationship('Book', backref='category', lazy=True)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    price_vnd = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    # N:1 với Category
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # N:M với Author
    authors = db.relationship('Author', secondary=book_authors, backref=db.backref('books', lazy='dynamic'))
    
    # 1:N với Review
    reviews = db.relationship('Review', backref='book', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'price_vnd': self.price_vnd,
            'stock': self.stock,
            'category': {
                'id': self.category.id,
                'name': self.category.name,
                'slug': self.category.slug
            } if self.category else None,
            'authors': [{'id': a.id, 'name': a.name} for a in self.authors]
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    
    # 1:N với Review
    reviews = db.relationship('Review', backref='user', lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)