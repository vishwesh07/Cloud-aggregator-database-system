from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'multicloud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

def sql_select(query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def sql_insert(query, var=None):
    cursor = conn.cursor()
    if var:
        cursor.execute(query, var)
    else:
        cursor.execute(query)
    conn.commit()

def sql_delete(query,var=None):
    cursor = conn.cursor()
    if var:
        cursor.execute(query, var)
    else:
        cursor.execute(query)
    conn.commit()

def sql_update(query, var=None):
    cursor = conn.cursor()
    if var:
        cursor.execute(query, var)
    else:
        cursor.execute(query)
    conn.commit()