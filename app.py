from os import error
from flask import render_template, request, url_for, Flask, redirect, session, jsonify
from flask.helpers import flash
from flask_pymongo import PyMongo
from pymongo import collection

app = Flask(__name__)
app.secret_key = "secret"

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
   print("redirected to questions")
   college_collection = mongo.db.NYSCollege
   colleges = list(college_collection.find({}))

   city_collection = mongo.db.NYSCities
   cities = list(city_collection.find({}))
   if (session.get('user')):
      user = session['user']
      print("found user in session")
      return render_template('questions.html', user = user, colleges = colleges, cities = cities)
   else:
      print("could not find user in session")
      return redirect(url_for('login'))

@app.route('/trips')
def trips():
   return render_template('trips.html')


@app.route('/login/', methods=["GET", "POST"])
def login():
   collection = mongo.db.userinfo
   if (request.method == "POST"):
      data = {
         "username" : request.form['username'],
         "password" : request.form['password']
      }
      if collection.find_one({"username": data['username']}) == None:
         flash("No account with that username exists. Please sign up to create an account.")
         return redirect(url_for("signup"))
      user = collection.find_one({"username": data['username']})
      if (user['password'] == data['password']):
         session['user'] = user
         return redirect(url_for('questions'))
      else:
         flash("Incorrect username/password.")
         return render_template('login.html')
   return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
   collection = mongo.db.userinfo
   if request.method == "POST":
      data = {
         "username": request.form['username'],
         "password": request.form['password'],
         "first_name": request.form['first_name'],
         "last_name": request.form['last_name'],
         "email": request.form['email'],
         "tel": request.form['tel']
      }
      
      if collection.find_one({"username": data['username']}) == None:
         collection.insert({"username": request.form['username'],
         "password": request.form['password'],
         "first_name": request.form['first_name'],
         "last_name": request.form['last_name'],
         "email": request.form['email'],
         "tel": request.form['tel']})

         session['user'] = data

         print("added user")
         return redirect(url_for('questions'))
      else:
         flash(f"An account with the username \"{data.get('username')}\" already exists")
         return redirect(url_for('signup'))
   return render_template('signup.html')
