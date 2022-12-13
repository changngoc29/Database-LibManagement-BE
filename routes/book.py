from flask import Blueprint, jsonify
from database import dbcursor

books = Blueprint("book",__name__,url_prefix="/api/v1/books")

@books.get('/')
def get_all_books():
    dbcursor.execute("SELECT * FROM book")
    results = dbcursor.fetchall()
    books = []
    for result in results:
        books.append(result)
    return jsonify(books)