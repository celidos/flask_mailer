from flask import Flask, request
from flask import render_template
import pika
from pika import PlainCredentials
from pymongo import MongoClient
from flask import Flask, redirect
from flask import Flask, session

app = Flask(__name__)

# Configure rabbitmq channel for publishing.
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672,
                                                               credentials=PlainCredentials('user', 'password')))
channel = connection.channel()
channel.queue_declare(queue='hello')

client = MongoClient('localhost', 27017)
db = client["users_database"]
users = db['users']

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        users.insert_one({"email": request.form["email"], "password": request.form["password"],
                          "is_active": False})
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=request.form["email"])
        return render_template('please_confirm.html')
    else:
        return render_template('registration_form.html')


@app.route('/', methods=['GET'])
def main():
    if 'username' in session.keys():
        print(session['username'])
        return render_template('top_secret.html', logged_in=True)
    else:
        return render_template('top_secret.html', logged_in=False)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = users.find_one({"email": request.form["email"], "password": request.form["password"]})
        print("logging in ", user)
        if user is None:
            return render_template('wrong_credentials.html')
        if not user['is_active']:
            return render_template('please_confirm.html')
        session['username'] = user['email']
        return redirect('/')
    else:
        return render_template('login_form.html')


@app.route('/confirm/<email>/', methods=['GET'])
def confirm(email):
    user = users.find_one({"email": email})
    if user is not None:
        users.update_one({'email': user['email'], 'is_active': False}, {'$set': {'is_active': True}})
    return render_template('confirmed.html')


@app.route('/logout/')
def logout():
    if 'username' in session.keys():
        session.clear()
    return redirect('/')
