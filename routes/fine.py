from flask import Blueprint, jsonify
from database import dbcursor
from datetime import datetime

fines = Blueprint("fines",__name__,url_prefix="/api/v1/fines")

@fines.get('/')
def get_all_fines():
    dbcursor.execute("SELECT * FROM finerecord")
    results = dbcursor.fetchall()
    fines = []
    for result in results:
        fine = {
            "fine_id": result[0],
            "num_of_day_late": result[1],
            "return_bill_id": result[2]
        }
        fines.append(fine)
    return jsonify(fines)