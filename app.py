from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
import sqlite3
import time

app = Flask(__name__)

# @app.route('/')
# def hello_world():

#     return render_template('index.html', )

@app.route('/<name>')
def hello_world(name):
    return f"<p>Hello, {escape(name)}!</p>"

@app.route('/collect', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['machine_name']
        gpu_usage = request.form['msi_usage']
        IP = request.form['I.P']
        user = request.form['user']
        time = request.form['time']
        machine = get_machine(IP)
        if machine :
            if get_last_session(machine[0]) :
                if gpu_usage == "0" :
                    close_sessino(IP)
            elif gpu_usage != "0" :
                add_session(machine[0], user, time)
        else :
            add_machine(name, IP)
            machine = get_machine(IP)
            add_session(machine[0], user, time)
        machine = get_machine(IP)
        session = get_last_session(machine[0])
        update_machine(IP, session, 1)
        add_log(session, gpu_usage, time)
        return "Good job"
    else:
        error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    machines = get_all_machines()
    ms = []
    for machine in machines :
        
        session  = get_last_session(machine[0])
        if session :
            if session[3] ==  0 :
                machina = {'id': machine[0], 'ip': machine[2], 'name': machine[1] , "gpu_usage": 0, "user": "-", "since": "-"}
            else :
                gpu_usage = session[4]
                user = session[5]
                since = session[2]
                machina = {'id': machine[0], 'ip': machine[2], 'name': machine[1] , "gpu_usage": gpu_usage, "user": user, "since": since}
        else :
            machina = {'id': machine[0], 'ip': machine[2], 'name': machine[1] , "gpu_usage": 0, "user": "-", "since": "-"}
        ms.append(machina)
    return render_template('index.html', machines=ms,error=error)

def get_machine(IP) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM machines WHERE IP = ?", (IP,))
    machine = cur.fetchone()
    connection.close()
    return machine

def add_machine(name, IP) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO machines (machine_name, ip, last_session_id) VALUES (?, ?, ?)", (name, IP, 0))
    connection.commit()
    connection.close()

def update_machine(IP, last_session) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("UPDATE machines SET last_session_id = ? WHERE IP = ?", (last_session[0], IP))
    connection.commit()
    connection.close()


def get_last_session(machine_id) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM machine_sessions WHERE machine_id = ? and is_current = ?", (machine_id, 1))
    session = cur.fetchone()
    connection.close()
    return session

def close_sessino(machine_id) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("UPDATE machine_sessions SET is_current = 0 WHERE machine_id = ? and is_current = ?", (machine_id, 1))
    connection.commit()
    connection.close()

def add_session(IP, user, time) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO machine_sessions (machine_id, user, is_current, start_time) VALUES (?, ?, ?, ?)", (IP, user, 1, time))
    connection.commit()
    connection.close()

def add_log(session, gpu_usage, time) :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO session_logs (session_id, log_time, gpu_usage) VALUES (?, ?, ?)", (session[0], time , gpu_usage))
    connection.commit()
    connection.close()

def get_all_machines() :
    connection = sqlite3.connect('machines.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM machines")
    machines = cur.fetchall()
    connection.close()
    return machines