from flask import Blueprint, jsonify
from database import mydb
from datetime import datetime
from flask_cors import CORS

fines = Blueprint("fines",__name__,url_prefix="/api/v1/fines")

@fines.get('/')
def get_all_fines():
    dbcursor = mydb.cursor()

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
    
    dbcursor.close()

    return jsonify(fines)