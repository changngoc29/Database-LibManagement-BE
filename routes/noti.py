from flask import Blueprint, jsonify, request
from database import mydb
from datetime import datetime
from flask_cors import CORS

notis = Blueprint("notis",__name__,url_prefix="/api/v1/notis")
CORS(notis)

@notis.get('/')
def get_all_notis():
    dbcursor = mydb.cursor()

    dbcursor.execute("SELECT * FROM notification")
    results = dbcursor.fetchall()
    notis = []
    for result in results:
        noti = {
            "noti_id": result[0],
            "status": bool(result[1]),
            "customer_id": result[2],
            "isbn": result[3]
        }
        notis.append(noti)
    
    dbcursor.close()

    return jsonify(notis)

@notis.post('/')
def create_noti():
    dbcursor = mydb.cursor()

    customer_id = request.get_json()["customerID"]
    isbn = request.get_json()["ISBN"]
    args = [customer_id, isbn]
    dbcursor.callproc("create_noti", args)
    mydb.commit()

    dbcursor.close()
    return request.json;