from flask import Flask, render_template, request, json, jsonify
from flaskext.mysql import MySQL
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug import generate_password_hash, check_password_hash
from crud import sql_select, sql_delete, sql_update, sql_insert
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'multicloud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# MongoDB configurations
# app.config['MONGO_DBNAME'] = 'multicloud'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/multicloud'
# mongodb = PyMongo(app)
client = MongoClient('mongodb://localhost:27017/')
mongodb = client['multicloud']


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showLogin')
def showLogin():
    return render_template('login.html')

@app.route('/showCustomerAccountDisplay')
def showCustomerAccountDisplay():
    return render_template('customerAccountDisplay.html')

@app.route('/showMachines')
def showMachines():
    return render_template('machines.html')

@app.route('/showOrderHistory')
def showOrderHistory():
    return render_template('orderHistory.html')

@app.route('/showBilling')
def showBilling():
    return render_template('billing.html')

@app.route('/showProfile')
def showProfile():
    return render_template('profile.html')

@app.route('/showHelp')
def showHelp():
    return render_template('help.html')

@app.route('/showCsp')
def showCsp():
    return render_template('csp.html')

@app.route('/showCspMachines')
def showCspMachines():
    return render_template('cspMachines.html')

@app.route('/showCspOrderHistory')
def showCspOrderHistory():
    return render_template('cspOrderHistory.html')

@app.route('/showCspProfile')
def showCspProfile():
    return render_template('cspProfile.html')

@app.route('/showCspHelp')
def showCspHelp():
    return render_template('cspHelp.html')

@app.route('/showCspBilling')
def showCspBilling():
    return render_template('cspBilling.html')

@app.route('/showAdmin')
def showAdmin():
    return render_template('admin.html')

@app.route('/showAdminMachines')
def showAdminMachines():
    return render_template('adminMachines.html')

@app.route('/showAdminOrder')
def showAdminOrder():
    return render_template('adminOrder.html')

@app.route('/showAdminCustomers')
def showAdminCustomers():
    return render_template('adminCustomers.html')

@app.route('/showAdminCSP')
def showAdminCSP():
    return render_template('adminCSP.html')

@app.route('/showAdminBilling')
def showAdminBilling():
    return render_template('adminBilling.html')

@app.route('/showAdminProfile')
def showAdminProfile():
    return render_template('adminProfile.html')

@app.route('/showAdminComplaints')
def showAdminComplaints():
    return render_template('adminComplaints.html')

@app.route('/showAdminOffer')
def showAdminOffer():
    return render_template('adminOffer.html')

@app.route('/myCSPs', methods=['GET'])
def myCSPs():
    try:
        _ca_id = request.args['inputCaId']
        if _ca_id:
            return json.dumps({'resultsAvailable': sql_select('select * from csp c join csp_contracts o on c.csp_id=o.csp_id where o.ca_id='+_ca_id+' and c.csp_id not in (select m.csp_id from machine m where m.order_id is not null)'),
                               'resultsOccupied': sql_select(
                                   'select * from csp c join csp_contracts o on c.csp_id=o.csp_id where o.ca_id=' + _ca_id + ' and c.csp_id in (select m.csp_id from machine m where m.order_id is not null)')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/myCustomers', methods=['GET'])
def myCustomers():
    try:
        _ca_id = request.args['inputCaId']
        if _ca_id:
            return json.dumps({'results': sql_select('select * from customer c join onboards o on c.customer_id=o.customer_id where c.customer_isDelete=0 and o.ca_id='+_ca_id)})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/currentOrders', methods=['GET'])
def currentOrders():
    try:
        _id = request.args['inputId']
        _role = request.args['inputRole']
        _ca_id = request.args['inputCaId']
        if _id and _ca_id and _role == "customer":
            return json.dumps({'results': sql_select('select * from order_customer where customer_id="'+_id+'" and ca_id="'+ _ca_id +'" and order_end_date is null')})
        elif _id and _ca_id and _role == "csp":
            print('select * from order_csp where csp_id="' + _id + '" and ca_id="' + _ca_id + '" and order_end_date is null')
            return json.dumps({'results': sql_select('select * from order_csp where csp_id="' + _id + '" and ca_id="' + _ca_id + '" and order_end_date is null')})
        elif _id and _ca_id and _role == "ca":
            return json.dumps({'results': sql_select('select * from order_ o join receives r on o.order_id=r.order_id where o.ca_id="' + _ca_id + '" and o.order_end_date is null')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/orderHistory', methods=['GET'])
def orderHistory():
    try:
        _id = request.args['inputId']
        _role = request.args['inputRole']
        _ca_id = request.args['inputCaId']
        if _id and _ca_id and _role == "customer":
            return json.dumps({'results': sql_select('select * from order_customer where customer_id="'+_id+'" and ca_id="'+ _ca_id +'" and order_end_date is not null')})
        elif _id and _ca_id and _role == "csp":
            return json.dumps({'results': sql_select('select * from order_csp where csp_id="' + _id + '" and ca_id="' + _ca_id + '" and order_end_date is not null')})
        elif _id and _ca_id and _role == "ca":
            print('select * from order_ o join receives r on o.order_id=r.order_id where o.ca_id="' + _ca_id + '" and o.order_end_date is not null')
            return json.dumps({'results': sql_select('select * from order_ o join receives r on o.order_id=r.order_id where o.ca_id="' + _ca_id + '" and o.order_end_date is not null')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/getMachines', methods=['GET'])
def getMachines():
    try:
        _id = request.args['inputId']
        _role = request.args['inputRole']
        _ca_id = request.args['inputCaId']
        if _id and _ca_id and _role == "customer":
            return json.dumps({'results': sql_select('select m.*, ord.ca_id from order_customer ord join machine_customer m on ord.order_id=m.order_id where ord.customer_id="'+_id+'" and ord.ca_id="'+ _ca_id +'" and order_end_date is null')})
        elif _id and _ca_id and _role == "csp":
            print('select m.* from order_csp r join machine m on r.order_id=m.order_id where r.csp_id="' + _id + '" and r.ca_id="' + _ca_id + '" and order_end_date is null')
            return json.dumps({'results': sql_select('select m.* from machine m where m.csp_id="' + _id + '";')})
        elif _id and _ca_id and _role == "ca":
            print('select * from order_ ord join machine m on ord.order_id=m.order_id where ord.ca_id="' + _ca_id + '" and order_end_date is null')
            return json.dumps({'results': sql_select('select m.*, ord.customer_id from order_ ord join machine m on ord.order_id=m.order_id where ord.ca_id="' + _ca_id + '" and order_end_date is null')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/bill/current', methods=['GET'])
def current_bill():
    try:
        _id = request.args['id']
        _role = request.args['role']
        if _id and _role == "customer":
            # print('select * from customer_bill where customer_id="'+_id+'"')
            return json.dumps({'results': sql_select('select * from customer_bill where customer_id="'+_id+'" and is_paid is False;')})
        elif _id and _role == "ca":
            return json.dumps({'results': sql_select('select * from ca_bill where ca_id="' + _id + '" and is_paid is False;')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/bill/history', methods=['GET'])
def bill_history():
    try:
        _id = request.args['id']
        _role = request.args['role']
        if _id and _role == "customer":
            return json.dumps({'results': sql_select('select * from customer_bill where customer_id="'+_id+'" and is_paid is True;')})
        elif _id and _role == "ca":
            return json.dumps({'results': sql_select('select * from ca_bill where ca_id="' + _id + '" and is_paid is True;')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/revenue/current', methods=['GET'])
def current_revenue():
    try:
        _id = request.args['id']
        _role = request.args['role']
        if _id and _role == "ca":
            # print('select * from customer_bill where customer_id="'+_id+'"')
            return json.dumps({'results': sql_select('select * from customer_bill where ca_id="'+_id+'" and is_paid is False;')})
        elif _id and _role == "csp":
            return json.dumps({'results': sql_select('select * from ca_bill where csp_id="' + _id + '" and is_paid is False;')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/revenue/history', methods=['GET'])
def revenue_history():
    try:
        _id = request.args['id']
        _role = request.args['role']
        if _id and _role == "ca":
            # print('select * from customer_bill where customer_id="'+_id+'"')
            return json.dumps(
                {'results': sql_select('select * from customer_bill where ca_id="' + _id + '" and is_paid is True;')})
        elif _id and _role == "csp":
            return json.dumps(
                {'results': sql_select('select * from ca_bill where csp_id="' + _id + '" and is_paid is True;')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/bill/generate', methods=['GET'])
def generate_bill():
    try:
        _id = request.args['id']
        _role = request.args['role']
        conn = mysql.connect()
        cursor = conn.cursor()
        messages = []
        if _id and _role == "ca":
            print(_id, _role)
            for ca_id, customer_id in sql_select('select order_.ca_id, order_.customer_id from onboards join order_ on order_.customer_id = onboards.customer_id and order_.ca_id = onboards.ca_id where order_.ca_id="' + _id + '";'):
                print("Generating bill for customer_id:", customer_id)
                cursor.callproc('sp_generate_bill_ca', (datetime.now().month, datetime.now().year, ca_id, customer_id))
                message = cursor.fetchall()
                if len(message):
                    print(message[0])
                    messages.append(message[0])
                    conn.commit()
                else:
                    return json.dumps({'Error': str(messages[0])}), 500
            return json.dumps({'message': messages})
        elif _id and _role == "csp":
            for csp_id, ca_id in sql_select('select receives.csp_id, order_.ca_id from receives join order_ on order_.order_id = receives.order_id where receives.csp_id="' + _id + '";'):
                print("Generating bill for ca_id:", ca_id)
                cursor.callproc('sp_generate_bill_csp', (datetime.now().month, datetime.now().year, csp_id, ca_id))
                message = cursor.fetchall()
                if len(message):
                    print(message[0])
                    messages.append(message[0])
                    conn.commit()
                else:
                    return json.dumps({'Error': str(messages[0])}), 500
            return json.dumps({'message': messages})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/bill/pay', methods=['POST'])
def pay_bill():
    try:
        _id = request.args['id']
        _role = request.args['role']
        _bill_id = request.args['bill_id']
        if _id and _role == "customer":
            sql_update('update bill set is_paid = True where customer_id=' + id + 'and bill_id=' + _bill_id + ' and is_paid = False;')
            return json.dumps({'results':"Bill:"+str(_bill_id)+"is paid by customer:"+str(_id)})
        elif _id and _role == "ca":
            sql_update('update bill set is_paid = True where ca_id=' + id + 'and bill_id=' + _bill_id + ' and is_paid = False;')
            return json.dumps({'results': "Bill:" + str(_bill_id) + "is paid by ca:" + str(_id)})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    try:
        _email = request.form['inputEmailLogin']
        _password = request.form['inputPasswordLogin']
        _role = request.args['inputRole']

        if _email and _role == "customer":
            userRow = sql_select('select customer_id, customer_email_id, customer_name, customer_password, customer_bank_account from customer where customer_email_id="'+_email+'"')
            if check_password_hash(userRow[0][3], _password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        elif _email and _role == "ca":
            userRow = sql_select('select ca_id, ca_email_id, ca_name, ca_password, ca_bank_account_number from ca where ca_email_id="'+_email+'"')
            if check_password_hash(userRow[0][3], _password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        elif _email and _role == "csp":
            userRow = sql_select('select csp_id, csp_email_id, csp_name, csp_password, csp_bank_account_number from csp where csp_email_id="'+_email+'"')
            if check_password_hash(userRow[0][3], _password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        else:
            return json.dumps({'error': 'Enter required fields'}), 500
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/placeOrder', methods=['POST'])
def placeOrder():
    try:
        _startDate = request.form['inputOrderStartDate']
        _ram = request.form['inputRam']
        _cpu = request.form['inputCpu']
        _diskSize = request.form['inputDiskSize']
        _noOfMahcines = request.form['inputNoOfMachines']
        _customer_id = request.args['customer_id']
        _ca_id = request.args['inputCaId']

        conn = mysql.connect()
        cursor = conn.cursor()

        if _startDate and _ram and _cpu and _diskSize and _noOfMahcines and _customer_id and _ca_id:
            cursor.callproc('sp_create_order', (_startDate, _ram, _cpu, _diskSize, _noOfMahcines, _customer_id, _ca_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'Order placed successfully !'})
            else:
                return json.dumps({'Error': str(data[0])}), 500
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _bank_account_number = request.form['inputBankAccount']
        _role = request.args['inputRole']
        _ca_id = request.args['inputCaId']

        conn = mysql.connect()
        cursor = conn.cursor()

        # validate the received values
        if _name and _email and _password and _bank_account_number and _ca_id:
            # All Good, let's call MySQL
            _hashed_password = generate_password_hash(_password)
            if _role == 'customer':
                cursor.callproc('sp_create_customer', (_email, _name, _hashed_password, _bank_account_number, _ca_id))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'User created successfully !'})
                else:
                    return json.dumps({'error': str(data[0])}), 500

            elif _role == 'csp':
                cursor.callproc('sp_create_csp', (_email, _name, _hashed_password, _bank_account_number, _ca_id))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'Csp created successfully !'})
                else:
                    return json.dumps({'error': str(data[0])}), 500

            elif _role == 'ca':
                cursor.callproc('sp_create_ca', (_email, _name, _hashed_password, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'Ca created successfully !'})
                else:
                    return json.dumps({'error': str(data[0])}), 500

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    # finally:
    #     cursor.close()
    #     conn.close()

@app.route('/updateProfile', methods = ['POST'])
def updateProfile():
    try:
        _id = request.args['inputId']
        _role = request.args['inputRole']
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _bank_account_number = request.form['inputBankAccount']
        _hashed_password = generate_password_hash(_password)
        conn = mysql.connect()
        cursor = conn.cursor()
        if _id and _role:
            if _role == 'csp':
                cursor.callproc('sp_update_csp', (_id, _email, _name, _hashed_password, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'results': { "_name" : _name, "_password" : _password, "_bank_account_number": _bank_account_number, "_hashed_password": _hashed_password}})
                else:
                    return json.dumps({'error': str(data[0])})
            elif _role == 'customer':
                print(request.form)
                cursor.callproc('sp_update_customer', (_id, _email, _name, _hashed_password, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'results': { "_name" : _name, "_password" : _password, "_bank_account_number": _bank_account_number, "_hashed_password": _hashed_password}})
                else:
                    return json.dumps({'error': str(data[0])})
            elif _role == 'ca':
                cursor.callproc('sp_update_ca', (_id, _email, _name, _hashed_password, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'results': { "_name" : _name, "_password" : _password, "_bank_account_number": _bank_account_number, "_hashed_password": _hashed_password}})
                else:
                    return json.dumps({'error': str(data[0])})
            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/updateCustomerProfile', methods = ['POST'])
def updateCustomerProfile():
    try:
        _id = request.args['inputId']
        _role = request.args['inputRole']
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _bank_account_number = request.form['inputBankAccount']
        _offer_id = request.form['inputOfferId']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _id and _role:
            if _role == 'customer':
                cursor.callproc('sp_update_customer_admin', (_id, _email, _name, _bank_account_number, _offer_id))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'results': {"_name": _name, "_bank_account_number": _bank_account_number}})
                else:
                    return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/help', methods=['POST'])
def help():
    try:
        _id = request.args['inputId']
        _role = request.args['inputRole']
        _problem_title = request.form['inputProblemTitle']
        _problem_description = request.form['inputProblemDescription']
        if _id and _role and _problem_title and _problem_description:
            record = {
                "id": _id,
                "role": _role,
                "problem_title": _problem_title,
                "problem_description": _problem_description,
                "date": datetime.utcnow(),
                "resolved": "no"
            }
            tickets = mongodb.tickets
            ticket_id = tickets.insert(record)
            # print(ticket_id, tickets.find_one({'_id': ticket_id}))
            # print(dict(tickets.find_one({'_id': ticket_id})))
            return jsonify({"result": "ticket created with id"+str(ticket_id)})
        else:
            return json.dumps({'error': 'Enter required fields'}), 500
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/getTickets', methods=['GET'])
def get_tickets():
    try:
        tickets_array = []
        id = request.args['inputId']
        role = request.args['inputRole']
        if id and role != "ca":
            tickets = mongodb.tickets
            user_tickets = tickets.find({"id":id, "role": role})
            for ticket in user_tickets:
                # print(dict(ticket))
                temp = dict()
                for key in ticket:
                    if key != '_id':
                        temp[key] = ticket[key]
                    else:
                        temp[key] = str(ticket[key])
                tickets_array.append(temp)
            return jsonify({"result":tickets_array})
        elif role == "ca":
            tickets = mongodb.tickets
            user_tickets = tickets.find()
            for ticket in user_tickets:
                temp = dict()
                for key in ticket:
                    if key != '_id':
                        temp[key] = ticket[key]
                    else:
                        temp[key] = str(ticket[key])
                tickets_array.append(temp)
            return jsonify({"result":tickets_array})
        else:
            return json.dumps({'error': 'Enter required fields'}), 500
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/resolveIssue', methods=['GET'])
def resolveIssue():
    try:
        _id = request.args['inputIssueId']
        if _id:
            mongodb.tickets.update({'_id': ObjectId(_id)}, {'$set': {"resolved": "yes"}}, upsert=False)
            return json.dumps({'msg': 'Issue resolved'})
        else:
            return json.dumps({'error': 'Enter required fields'}), 500
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/createOffer', methods = ['POST'])
def createOffer():
    try:
        _id = request.args['inputId']
        _name = request.form['inputName']
        _discount = request.form['inputDiscount']
        sql_insert('insert into offer (offer_name, discount, ca_id, is_used ) values ( "'+ _name +'", ' + _discount + ', '+_id+',0);')
        return json.dumps({'message': 'Offer created successfully !'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/getOffer', methods = ['GET'])
def getOffer():
    try:
        _ca_id = request.args['inputCaId']
        _customer_id = request.args['inputId']
        _role = request.args['inputRole']
        if _ca_id and _role:
            if _role == 'ca':
                return json.dumps({'results': sql_select('select * from offer where ca_id = '+ _ca_id +';')})
            if _role == 'customer':
                return json.dumps({'results': sql_select('select * from customer c join offer o on c.customer_offer_id=o.offer_id where  c.customer_id = '+ _customer_id +';')})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/deleteOffer', methods = ['DELETE'])
def deleteOffer():
    try:
        _offer_id = request.args['offerId']
        if _offer_id:
            return json.dumps({'results': sql_delete('delete from offer where offer_id = '+ _offer_id +';')})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/endOrder', methods = ['GET'])
def endOrder():
    try:
        _order_id = request.args['orderId']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _order_id:
            cursor.callproc('sp_end_order', (_order_id, _order_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'html': '<span>Order Ended</span>'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/addMachine', methods = ['POST'])
def addMachine():
    print(request.form)
    try:
        _csp_id = request.args['inputId']
        _ip_address = request.form['inputIpAddress']
        _ram = request.form['inputRam']
        _disk_size = request.form['inputDiskSize']
        _price = request.form['inputPrice']
        _cpu_cores = request.form['inputCpuCores']
        sql_insert('insert into machine (csp_id, disk_size, ram, cpu_cores, ip_address, price, order_id ) values ( "'+ _csp_id +'", "' + _disk_size + '", '+_ram+', '+_cpu_cores+', "'+_ip_address+'", '+_price+',null);')
        return json.dumps({'message': 'Machine created successfully !'})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/deleteMachine', methods = ['DELETE'])
def deleteMachine():
    try:
        _mac_id = request.args['inputId']
        if _mac_id:
            return json.dumps({'results': sql_delete('delete from machine where mac_id = '+ _mac_id +';')})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/deleteCustomer', methods = ['DELETE'])
def deleteCustomer():
    try:
        _customer_id = request.args['inputId']
        if _customer_id:
            return json.dumps({'results': sql_delete('update customer set customer_isDelete=true where customer_id = '+ _customer_id +';')})
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)