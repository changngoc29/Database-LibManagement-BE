from flask import Blueprint, jsonify
from database import dbcursor
from datetime import datetime

payments = Blueprint("payments",__name__,url_prefix="/api/v1/payments")

@payments.get('/')
def get_all_payments():
    dbcursor.execute("SELECT * FROM payment")
    results = dbcursor.fetchall()
    payments = []
    for result in results:
        payment = {
            "payment_id": result[0],
            "payment_time": result[1].strftime('%Y-%m-%d %H:%M:%S'),
            "amount_money": result[2],
            "customer_id": result[3]
        }
        payments.append(payment)
    return jsonify(payments)

@payments.get('/<type>')
def get_all_specific_payments(type):
    payments = []
    if type=="fine":
        dbcursor.execute("select * from finepayment bp left join payment p on bp.Payment_ID=p.Payment_ID;")
        results = dbcursor.fetchall()
        for result in results:
            payment = {
                "payment_id": result[0],
                "fine_id": result[1],
                "payment_time": result[3].strftime('%Y-%m-%d %H:%M:%S'),
                "amount_money": result[4],
                "customer_id": result[5]
            }
            payments.append(payment)
    else:
        dbcursor.execute("select * from borrowhomepayment bp left join payment p on bp.Payment_ID=p.Payment_ID;")
        results = dbcursor.fetchall()
        for result in results:
            payment = {
                "payment_id": result[0],
                "loan_bill_id": result[1],
                "payment_time": result[3].strftime('%Y-%m-%d %H:%M:%S'),
                "amount_money": result[4],
                "customer_id": result[5]
            }
            payments.append(payment)
    return jsonify(payments)