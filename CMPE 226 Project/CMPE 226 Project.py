from flask import Flask, render_template, request, json, jsonify
from flaskext.mysql import MySQL
from flask_pymongo import PyMongo
from werkzeug import generate_password_hash, check_password_hash
from crud import sql_select, sql_delete, sql_update, sql_insert

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'multicloud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# MongoDB configurations
app.config['MONGO_DBNAME'] = 'multicloud'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/multicloud'

mongo = PyMongo(app)

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

@app.route('/bills', methods=['GET'])
def bill():
    try:
        _customer_id = request.args['customer_id']
        if _email and _role == "customer":
            print('select * from bill where customer_id="'+_customer_id+'"')
            return json.dumps({'results': sql_select('select * from bill where customer_id="'+_customer_id+'"')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
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
    print(request.args)
    print(request.form)
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
                    return json.dumps({'message': 'CSP updated successfully !'})
                else:
                    return json.dumps({'error': str(data[0])})
            elif _role == 'customer':
                cursor.callproc('sp_update_customer', (_id, _email, _name, _hashed_password, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'Customer updated successfully !'})
                else:
                    return json.dumps({'error': str(data[0])})
            elif _role == 'ca':
                cursor.callproc('sp_update_ca', (_id, _email, _name, _hashed_password, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'CA updated successfully !'})
                else:
                    return json.dumps({'error': str(data[0])})
            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
