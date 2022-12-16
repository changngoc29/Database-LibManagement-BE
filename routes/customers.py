from flask import Blueprint, jsonify
from flask_cors import CORS
from database import mydb

customers = Blueprint("customers", __name__, url_prefix="/api/v1/customers")
CORS(customers)

@customers.get('/')
def get_all_customers():
    dbcursor = mydb.cursor()

    dbcursor.execute("SELECT * FROM customer")
    results = dbcursor.fetchall()
    customers = []
    for result in results:
        customers.append(result)
    
    dbcursor.close()
    
    return jsonify(customers)