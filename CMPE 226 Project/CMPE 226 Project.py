from flask import Flask, render_template, request, json, jsonify
from flaskext.mysql import MySQL
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug import generate_password_hash, check_password_hash
from crud import sql_select, sql_delete, sql_update, sql_insert
from datetime import datetime

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

@app.route('/showAdmin')
def showAdmin():
    return render_template('admin.html')

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

@app.route('/showAdminCustomer')
def showAdminCustomer():
    return render_template('adminCustomer.html')

@app.route('/showCspBilling')
def showCspBilling():
    return render_template('cspBilling.html')

@app.route('/myCSPs', methods=['GET'])
def myCSPs():
    try:
        _ca_id = request.args['inputCaId']
        if _ca_id:
            return json.dumps({'results': sql_select('select * from csp c join csp_contracts o on c.csp_id=o.csp_id')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/myCustomers', methods=['GET'])
def myCustomers():
    try:
        _ca_id = request.args['inputCaId']
        if _ca_id:
            return json.dumps({'results': sql_select('select * from customer c join onboards o on c.customer_id=o.customer_id')})
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
            print('select * from order_customer where customer_id="'+_id+'" and ca_id="'+ _ca_id +'" and order_end_date is null')
            return json.dumps({'results': sql_select('select * from order_customer where customer_id="'+_id+'" and ca_id="'+ _ca_id +'" and order_end_date is null')})
        elif _id and _ca_id and _role == "csp":
            return json.dumps({'results': sql_select('select * from order_csp where csp_id="' + _id + '" and ca_id="' + _ca_id + '" and order_end_date is null')})
        elif _id and _ca_id and _role == "ca":
            print('select * from order_ where ca_id="' + _ca_id + '" and order_end_date is null')
            return json.dumps({'results': sql_select('select * from order_ where ca_id="' + _ca_id + '" and order_end_date is null')})
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
            return json.dumps({'results': sql_select('select * from order_ where ca_id="' + _ca_id + '" and order_end_date is not null')})
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
            for ca_id, customer_id in sql_select('select * from onboards join order_ on order_.customer_id = onboards.customer_id and order_.ca_id = onboards.ca_id where ca_id="' + _id + '";'):
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
            userRow = sql_select('select * from customer where customer_email_id="'+_email+'"')
            if check_password_hash(userRow[0][3], _password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        elif _email and _role == "ca":
            userRow = sql_select('select * from ca where ca_email_id="'+_email+'"')
            if check_password_hash(userRow[0][4], _password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        elif _email and _role == "csp":
            userRow = sql_select('select * from csp where csp_email_id="'+_email+'"')
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
    print(request.form)
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

@app.route('/help', methods=['POST'])
def help():
    try:
        email = request.args['email']
        role = request.args['role']
        problem_title = request.form['problemTitle']
        problem_description = request.form['problemDescription']
        if email and role and problem_title and problem_description:
            record = {
                "email": email,
                "role": role,
                "problem_title": problem_title,
                "problem_description": problem_description,
                "date": datetime.datetime.utcnow(),
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
        email = request.args['email']
        role = request.args['role']
        if email and role:
            tickets = mongodb.tickets
            user_tickets = tickets.find({"email":email, "role": role})
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
        else:
            return json.dumps({'error': 'Enter required fields'}), 500
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
