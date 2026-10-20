from flask import Flask
from models import db, Category, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from routes.books import books_bp
app.register_blueprint(books_bp, url_prefix='/api/v1')

def seed_data():
    if Category.query.count() == 0:
        cat_fiction = Category(name='Fiction', slug='fiction')
        cat_scifi = Category(name='Sci-Fi', slug='scifi')
        
        author1 = Author(name='J.K. Rowling', bio='Author of Harry Potter')
        author2 = Author(name='George Orwell', bio='Author of 1984')
        
        db.session.add_all([cat_fiction, cat_scifi, author1, author2])
        db.session.commit()

        b1 = Book(title='1984', isbn='1111111111', price_vnd=120000, stock=50, category=cat_fiction, authors=[author2])
        b2 = Book(title='Animal Farm', isbn='2222222222', price_vnd=90000, stock=30, category=cat_fiction, authors=[author2])
        b3 = Book(title='Sci-Fi Adventure', isbn='3333333333', price_vnd=150000, stock=20, category=cat_scifi, authors=[author1])
        
        db.session.add_all([b1, b2, b3])
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)