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

def sql_insert(query, var):
    cursor = conn.cursor()
    cursor.execute(query, var)
    conn.commit()

def sql_delete(query):
    cursor = conn.cursor()
    cursor.execute(query, var)

def sql_update(query, var):
    cursor = conn.cursor()
    cursor.execute(query, var)
    rows = cursor.fetchall()
    return rows