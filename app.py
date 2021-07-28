from inspect import FullArgSpec
from os import error
from flask import render_template, request, url_for, Flask, redirect, session, jsonify
from flask.helpers import flash
from flask_pymongo import PyMongo, ObjectId
from pymongo import collection, database

app = Flask(__name__)
app.secret_key = "secret"

app.config['MONGO_DBNAME'] = 'Collride'
app.config['MONGO_URI'] = 'mongodb+srv://admin:QBD7PhUMLLi59Fx9@cluster0.jtwfi.mongodb.net/Collride?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
def index():
    collection = mongo.db.userinfo
    data = list(collection.find({}))
    return render_template('home.html', data = data)


@app.route('/questions', methods=["GET", "POST"])
def questions():
   if (request.method == "POST"):
      userinfo = mongo.db.userinfo
      curr_username = session['user']['username']
      database_user = userinfo.find_one({'username': curr_username})

      # Add user info
      userinfo.update_one({"username": curr_username}, {"$set": {"college": request.form['college'], "city": request.form['city']}})

      if (request.form['car'] == "Yes"):
         userinfo.update_one({"username": curr_username}, {"$set": {"car": True}})
      else:
         userinfo.update_one({"username": curr_username}, {"$set": {"car": False}})

      print("added user info")

      setUserColCity(database_user)

      print("updated session user info")
      print("updated session user info")
      print("updated session user info")

      return redirect(url_for("trips"))

   else:
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

@app.route('/trips', methods=["GET", "POST"])
def trips():
   collection = mongo.db.userinfo
   if request.method == "POST":
      user = collection.find_one({'username': session['user']['username']})
      start = request.form["start"]
      end = request.form["end"]
      date = request.form["date"]

      collection.update_one({"username": session['user']['username']}, {"$set": {"start": start, "end": end, "date": date}})
      setUserColCity(user)

      similar_trips = list(collection.find({"start": start, "end": end}))
      
      for trip in similar_trips:
         if trip.get("username") == session['user']['username']:
            similar_trips.remove(trip)
      
      return render_template("trips.html", similar_trips = similar_trips, request = request)

   else:
      if session.get('user'):
         user = collection.find_one({"username": session['user']['username']})
         print("redirected to trips")
         setUserColCity(user)
         return render_template('trips.html')
      else:
         return redirect(url_for('login'))



@app.route('/login/', methods=["GET", "POST"])
def login():
   collection = mongo.db.userinfo
   if (request.method == "POST"):
      data = {
         "username" : request.form['username'],
         "password" : request.form['password']
      }
      print("went to login")
      if collection.find({"username": data['username']}) == None:
         print("did not find user")
         flash("No account with that username exists. Please sign up to create an account.")
         return redirect(url_for("signup"))
      user = collection.find_one({"username": data['username']})
      print(user)
      if (user['password'] == data['password']):
         print("correct password")
         
         setUserColCity(user)

         return redirect(url_for('trips'))
      else:
         print('incorrect password')
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
         "address": request.form['address'],
         "email": request.form['email'],
         "tel": request.form['tel']
      }
      
      if collection.find_one({"username": data['username']}) == None:
         collection.insert({"username": request.form['username'],
         "password": request.form['password'],
         "first_name": request.form['first_name'],
         "last_name": request.form['last_name'],
         "address": request.form['address'],
         "email": request.form['email'],
         "tel": request.form['tel']})

         session['user'] = {"username": request.form['username'],
         "password": request.form['password'],
         "first_name": request.form['first_name'],
         "last_name": request.form['last_name'],
         "address": request.form['address'],
         "email": request.form['email'],
         "tel": request.form['tel']}

         print("added user")
         return redirect(url_for('questions'))
      else:
         flash(f"An account with the username \"{data.get('username')}\" already exists")
         return redirect(url_for('signup'))
   return render_template('signup.html')

def setUserColCity(user):
   session['user'] = {"username": user['username'],
   "password": user['password'],
   "first_name": user['first_name'],
   "last_name": user['last_name'],
   "address": user['address'],
   "email": user['email'],
   "tel": user['tel']}

   if user['college']:
      session['user']['college'] = user['college']
      session['user']['city'] = user['city']
      session['user']['car'] = user['car']

   if user.get('start'):
      session['user']['start'] = user['start']
      session['user']['end'] = user['end']
      session['user']['date'] = user['date']

      