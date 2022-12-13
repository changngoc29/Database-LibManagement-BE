from flask import Flask, jsonify
from routes.book import books


app = Flask(__name__)

app.register_blueprint(books)

@app.get('/')
def index():
    return jsonify({"data": "homepage"})