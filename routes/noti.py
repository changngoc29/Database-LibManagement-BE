from flask import Blueprint, jsonify, request
from database import dbcursor, mydb
from datetime import datetime

notis = Blueprint("notis",__name__,url_prefix="/api/v1/notis")
@notis.get('/')
def get_all_notis():
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
    return jsonify(notis)

@notis.post('/')
def create_noti():
    customer_id = request.get_json()["customerID"]
    isbn = request.get_json()["ISBN"]
    args = [customer_id, isbn]
    dbcursor.callproc("create_noti", args)
    mydb.commit()
    return request.json;