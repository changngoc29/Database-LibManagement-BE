from flask import Blueprint, jsonify
from database import dbcursor

customers = Blueprint("customers", __name__, url_prefix="/api/v1/customers")

@customers.get('/')
def get_all_customers():
    dbcursor.execute("SELECT * FROM customer")
    results = dbcursor.fetchall()
    customers = []
    for result in results:
        customers.append(result)
    return jsonify(customers)