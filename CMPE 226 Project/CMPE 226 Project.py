from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from crud import sql_select, sql_delete, sql_update, sql_insert

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'multicloud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

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

@app.route('/myCSPs', methods=['GET'])
def myCSPs():
    try:
        ca_id = request.args['ca_id']
        if ca_id:
            return json.dumps({'results': sql_select('select * from Csp')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/myCustomers', methods=['GET'])
def myCustomers():
    try:
        ca_id = request.args['ca_id']
        if ca_id:
            return json.dumps({'results': sql_select('select * from customer')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/orders', methods=['GET'])
def orders():
    try:
        customer_id = request.args['customer_id']
        if customer_id:
            return json.dumps({'results': sql_select('select * from ORD where customer_id="'+customer_id+'"')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/bill', methods=['GET'])
def bill():
    try:
        ca_id = request.args['ca_id']
        if ca_id:
            return json.dumps({'results': sql_select('select * from Csp')})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    try:
        email = request.form['inputEmailLogin']
        password = request.form['inputPasswordLogin']
        role = request.args['role']

        if email and role == "customer":
            userRow = sql_select('select * from customer where email_id="'+email+'"')
            if check_password_hash(userRow[0][3], password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        elif email and role == "ca":
            userRow = sql_select('select * from ca where email_id="'+email+'"')
            if check_password_hash(userRow[0][3], password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        elif email and role == "csp":
            userRow = sql_select('select * from csp where email_id="'+email+'"')
            if check_password_hash(userRow[0][3], password):
                return json.dumps({'results': userRow})
            else:
                return json.dumps({'error': 'Invalid password'}), 500
        else:
            return json.dumps({'error': 'Enter required fields'}), 500
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _join_date = request.form['inputJoinDate']
        _bank_account_number = request.form['inputBankAccount']
        _role = request.form['inputRole']

        conn = mysql.connect()
        cursor = conn.cursor()

        # validate the received values
        if _name and _email and _password and _join_date and _bank_account_number:

            # All Good, let's call MySQL

            _hashed_password = generate_password_hash(_password)
            if _role == 'user':
                cursor.callproc('sp_createUser', (_email, _name, _hashed_password, _join_date, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'User created successfully !'})
                else:
                    return json.dumps({'error': str(data[0])})

            elif _role == 'csp':
                cursor.callproc('sp_createCsp', (_email, _name, _hashed_password, _join_date, _bank_account_number))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message': 'Csp created successfully !'})
                else:
                    return json.dumps({'error': str(data[0])})

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    # finally:
    #     cursor.close()
    #     conn.close()

if __name__ == '__main__':
    app.run(debug=True)
