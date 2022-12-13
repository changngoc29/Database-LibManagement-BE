from flask import Blueprint, jsonify
from database import dbcursor

staffs = Blueprint("staffs", __name__, url_prefix="/api/v1/staffs")

@staffs.get('/')
def get_all_staffs():
    dbcursor.execute("SELECT * FROM staff")
    results = dbcursor.fetchall()
    staffs = []
    for result in results:
        staffs.append(result)
    return jsonify(staffs)