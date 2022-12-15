from flask import Blueprint, jsonify
from database import dbcursor
from datetime import datetime

bills = Blueprint("bills",__name__,url_prefix="/api/v1/bills")

@bills.get('/loan')
def get_loan():
    dbcursor.execute("SELECT * FROM loanbill")
    results = dbcursor.fetchall()
    bills = []
    for result in results:
        bill = {
            "loan_bill_id": result[0],
            "staff_id": result[1],
            "customer_id": result[2],
            "book_id": result[3]
        }
        bills.append(bill)
    return jsonify(bills)

@bills.get('/loan/<type>')
def get_type_loan(type):
    bills = []
    if type=="home":
        dbcursor.execute("select * from borrowhomebill bb left join loanbill lb on bb.Loan_Bill_ID=lb.Loan_Bill_ID; ")
        results = dbcursor.fetchall()
        for result in results:
            bill = {
                "loan_bill_id": result[0],
                "staff_id": result[4],
                "customer_id": result[5],
                "book_id": result[6],
                "borrow_time": result[1].strftime('%Y-%m-%d %H:%M:%S'),
                "due_time": result[2].strftime('%Y-%m-%d %H:%M:%S')
            }
            bills.append(bill)
    else:
        dbcursor.execute("select * from readinlibrarybill rb left join loanbill lb on rb.Loan_Bill_ID=lb.Loan_Bill_ID;")
        results = dbcursor.fetchall()
        for result in results:
            bill = {
                "loan_bill_id": result[0],
                "staff_id": result[4],
                "customer_id": result[5],
                "book_id": result[6],
                "borrow_time": result[1].strftime('%Y-%m-%d %H:%M:%S'),
                "due_time": result[2].strftime('%Y-%m-%d %H:%M:%S')
            }
            bills.append(bill)
    return bills


