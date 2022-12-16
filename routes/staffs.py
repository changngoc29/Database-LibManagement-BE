from flask import Blueprint, jsonify
from flask_cors import CORS
from database import mydb

staffs = Blueprint("staffs", __name__, url_prefix="/api/v1/staffs")
CORS(staffs)

@staffs.get('/')
def get_all_staffs():
    dbcursor = mydb.cursor()
    
    dbcursor.execute("SELECT * FROM staff")
    results = dbcursor.fetchall()
    staffs = []
    for result in results:
        staffs.append(result)

    dbcursor.close()    
    return jsonify(staffs)