from flask import Flask, render_template, url_for, redirect, session, request, abort
from flask_mysqldb import MySQL
import MySQLdb
import handlers
import logging

app = Flask(__name__)
app.secret_key = "12345"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "test"

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("MainPage.html"), 200


# MAIN PAGE
@app.route("/Mainpage", methods=['GET', 'POST'])
def MainPage():
    return render_template('MainPage.html'), 200


# SHOW ALL CONFIGS:
@app.route("/Configs", methods=['GET', 'POST'])
def configs():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM configurations")
    confs = cur.fetchall()
    return render_template('Configs.html', confs=confs)


# SHOW CONF FOR SPECIFIC MODEL
@app.route('/<sensor_model>')
def specConfig(sensor_model):
    cur = db.connection.cursor()
    cur.execute("SELECT configuration_id, model_name,output,handler FROM configurations where model_name = %s",
                [sensor_model])
    conf = cur.fetchall()
    return render_template('SpecificSensor.html', conf=conf, sensor_model=sensor_model), 200


# CREATE NEW CONFIG, ERROR WHEN MODEL EXISTS
@app.route('/create/<model>/<output>/<handler>')
def create(model=None, handler=None, output=None):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    # info = cur.fetchone()
    cur.execute("SELECT * from configurations WHERE model_name= %s", [model])
    info = cur.fetchone()
    if info is not None:
        return 'Error!', 400
    else:
        cur.execute("INSERT INTO configurations(model_name,handler,output) VALUES (%s,%s,%s)", (model, handler, output))
        db.connection.commit()
        return 'OK!', 200;

# MESSAGES HANDLING
@app.route('/Handleit/<string:model>/<string:handler>/<string:output>')
def handleIt(model=None, handler=None, output=None):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * from sensors WHERE model= %s", [model])
    info = cur.fetchone()
    if model == 'WS-0001':
        logging.error(str(info.get('payload')))  # output always in logging
        return "Created", 201;

    elif model == 'WS-0002':
        output = 'console'
        return handlers.padToMultiple(info, output)
        # output and handler  always the same

    elif model == 'WS-0003':
        output = 'file'  # output will be always to file
        if handler == 'trim':
            return handlers.trim(info, output)
        elif handler == 'padtomultiple':
            return handlers.padToMultiple(info, output)
        else:
            return 'Not found!', 404

    elif model == 'WS-0004':
        if handler == 'trim':
            return handlers.trim(info, output)

        elif handler == 'padtomultiple':
            return handlers.padToMultiple(info, output)

        elif handler == 'timestamp':
            return handlers.addTimestamp(info, output)

        else:
            return 'Not found!', 404
    else:
        return 'Not found!', 404