from flask import Blueprint, jsonify
from database import mydb
from flask_cors import CORS

books = Blueprint("books",__name__,url_prefix="/api/v1/books")
CORS(books)

@books.get('/')
def get_all_books():
    dbcursor = mydb.cursor()

    dbcursor.execute("SELECT * FROM book b LEFT JOIN book_remainder br ON b.ISBN=br.ISBN; ")
    results = dbcursor.fetchall()
    books = []
    for result in results:
        books.append(result)
    
    dbcursor.close()
    return jsonify(books)
