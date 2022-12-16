from flask import Blueprint, jsonify, request
from database import mydb
from flask_cors import CORS
from datetime import datetime

bills = Blueprint("bills",__name__,url_prefix="/api/v1/bills")
CORS(bills)

@bills.get('/loan')
def get_loan():
    dbcursor = mydb.cursor()

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

    dbcursor.close()
    
    return jsonify(bills)

@bills.post('/loan')
def create_loan_bill():
    dbcursor = mydb.cursor()

    staff_id = request.get_json()["staffID"]
    customer_id = request.get_json()["customerID"]
    isbn = request.get_json()["ISBN"]
    typee = request.get_json()["type"]
    args = [staff_id, customer_id, isbn]
    if typee=="borrowHome":
        dbcursor.callproc("create_borrowhome_bill", args)
    else:
        dbcursor.callproc("create_readinlibrary_bill", args)
    mydb.commit()

    dbcursor.close()

    return request.json;

@bills.get('/loan/<type>')
def get_type_loan(type):
    dbcursor = mydb.cursor()

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

    dbcursor.close()
        
    return jsonify(bills)

@bills.get('/return')
def get_return_bill():
    dbcursor = mydb.cursor()

    dbcursor.execute("SELECT * FROM returnbill")
    results = dbcursor.fetchall()
    bills = []
    for result in results:
        bill = {
            "return_bill_id": result[0],
            "return date": result[1].strftime('%Y-%m-%d %H:%M:%S'),
            "loan_bill_id": result[2],
            "staff_id": result[3],
            "customer_id": result[4]
        }
        bills.append(bill)

    dbcursor.close()


    return jsonify(bills)

@bills.post('/return')
def create_return_bill():
    dbcursor = mydb.cursor()

    staff_id = request.get_json()["staffID"]
    customer_id = request.get_json()["customerID"]
    loan_bill_id = request.get_json()["loanbillID"]
    args = [staff_id, customer_id, loan_bill_id]
    dbcursor.callproc("create_return_bill", args)
    mydb.commit()

    dbcursor.close()
    return request.json;