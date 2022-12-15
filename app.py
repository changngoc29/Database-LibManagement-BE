from flask import Flask, jsonify
from routes.books import books
from routes.customers import customers
from routes.staffs import staffs
from flask_cors import CORS
from routes.bill import bills
from routes.fine import fines
from routes.payment import payments

app = Flask(__name__)
CORS(app)

app.register_blueprint(books)
app.register_blueprint(customers)
app.register_blueprint(staffs)
app.register_blueprint(bills)
app.register_blueprint(fines)
app.register_blueprint(payments)

@app.get('/')
def index():
    return jsonify({"data": "homepage"})