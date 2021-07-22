from typing import Collection
from flask import Flask, url_for
from flask import render_template
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Collride'
app.config['MONGO_URI'] = 'mongodb+srv://admin:QBD7PhUMLLi59Fx9@cluster0.jtwfi.mongodb.net/Collride?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
@app.route('/index')

def index():
    collection = mongo.db.userinfo
    data = list(collection.find({}))
    return render_template('base.html', data = data)

@app.route('/questions')
def questions():
   return render_template('questions.html')

@app.route('/trips')
def trips():
   return render_template('trips.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')