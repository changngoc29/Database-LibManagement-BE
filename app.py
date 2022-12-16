from flask import Flask, jsonify, request
from routes.books import books
from routes.customers import customers
from routes.staffs import staffs
from flask_cors import CORS
from routes.bill import bills
from routes.fine import fines
from routes.payment import payments
from routes.noti import notis
from database import mydb

app = Flask(__name__)
CORS(app)

is_querying = False


@app.get('/')
def index():
    return jsonify({"data": "homepage"})

# app.register_blueprint(books)
@app.get('/api/v1/books/')
def get_all_books():
    global is_querying
    while is_querying==True: {}
    is_querying = True
    dbcursor = mydb.cursor()

    dbcursor.execute("SELECT * FROM book b LEFT JOIN book_remainder br ON b.ISBN=br.ISBN; ")
    results = dbcursor.fetchall()
    books = []
    for result in results:
        books.append(result)
    
    dbcursor.close()
    is_querying = False
    return jsonify(books)

# app.register_blueprint(customers)
@app.get('/api/v1/customers/')
def get_all_customers():
    global is_querying
    while is_querying==True: {}
    is_querying = True
    dbcursor = mydb.cursor()

    dbcursor.execute("SELECT * FROM customer")
    results = dbcursor.fetchall()
    customers = []
    for result in results:
        customers.append(result)
    
    dbcursor.close()
    is_querying = False
    return jsonify(customers)

# app.register_blueprint(staffs)
@app.get('/api/v1/staffs/')
@staffs.get('/')
def get_all_staffs():
    global is_querying
    while is_querying==True: {}
    is_querying = True
    dbcursor = mydb.cursor()
    
    dbcursor.execute("SELECT * FROM staff")
    results = dbcursor.fetchall()
    staffs = []
    for result in results:
        staffs.append(result)

    dbcursor.close()  
    is_querying = False  
    return jsonify(staffs)

# app.register_blueprint(bills)
@app.get('/api/v1/bills/loan')
def get_loan():
    global is_querying
    while is_querying==True: {}
    is_querying = True

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

    is_querying = False
    
    return jsonify(bills)

@app.post('/api/v1/bills/loan')
def create_loan_bill():
    global is_querying
    while is_querying==True: {}
    is_querying = True

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

    is_querying = False

    return request.json;

@app.get('/api/v1/bills/loan/<type>')
def get_type_loan(type):
    global is_querying
    while is_querying==True: {}
    is_querying = True

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

    is_querying = False
        
    return jsonify(bills)

@app.get('/api/v1/bills/return')
def get_return_bill():
    global is_querying
    while is_querying==True: {}
    is_querying = True
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

    is_querying = False

    return jsonify(bills)

@app.post('/api/v1/bills/return')
def create_return_bill():
    global is_querying
    while is_querying==True: {}
    is_querying = True

    dbcursor = mydb.cursor()

    staff_id = request.get_json()["staffID"]
    customer_id = request.get_json()["customerID"]
    loan_bill_id = request.get_json()["loanbillID"]
    args = [staff_id, customer_id, loan_bill_id]
    dbcursor.callproc("create_return_bill", args)
    mydb.commit()

    dbcursor.close()
    is_querying = False
    return request.json;

# app.register_blueprint(fines)
@app.get('/api/v1/fines/')
def get_all_fines():
    global is_querying
    while is_querying==True: {}
    is_querying = True
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

    is_querying = False

    return jsonify(fines)

# app.register_blueprint(payments)
@app.get('/api/v1/payments')
def get_all_payments():
    global is_querying
    while is_querying==True: {}
    is_querying = True

    dbcursor = mydb.cursor()

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

    dbcursor.close()

    is_querying = False

    return jsonify(payments)

@app.get('/api/v1/payments/<type>')
def get_all_specific_payments(type):
    global is_querying
    while is_querying==True: {}
    is_querying = True

    dbcursor = mydb.cursor()

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
    dbcursor.close()

    is_querying = False
    return jsonify(payments)

# app.register_blueprint(notis)
@app.get('/api/v1/notis')
def get_all_notis():
    global is_querying
    while is_querying==True: {}
    is_querying = True

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

    is_querying = False

    return jsonify(notis)

@app.post('/api/v1/notis')
def create_noti():
    global is_querying
    while is_querying==True: {}
    is_querying = True

    dbcursor = mydb.cursor()

    customer_id = request.get_json()["customerID"]
    isbn = request.get_json()["ISBN"]
    args = [customer_id, isbn]
    dbcursor.callproc("create_noti", args)
    mydb.commit()

    dbcursor.close()

    is_querying = False

    return request.json;
