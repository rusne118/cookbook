import os
from flask import Flask, render_template, flash, redirect, request, url_for, session, make_response, current_app
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'cookbook'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00t@cookbook-k2dbu.mongodb.net/cookbook?retryWrites=true'

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html', meals=mongo.db.meals.find())

@app.route('/dinner')
def dinner():
    return render_template('dinner.html', meals=mongo.db.meals.find())

@app.route('/dessert')
def dessert():
    return render_template('dessert.html', meals=mongo.db.meals.find())

@app.route('/login', methods=["POST", "GET"])
def login():
    users = mongo.db.users
    login_user = users.find_one({"username" : request.form.get("username", False)})
    if login_user:
        if (request.form['pass']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash('Invalid username/password combination')

    return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({"username" : request.form['username']})
        if existing_user is None:
            users.insert({'username' : request.form['username'],
                            'password' : request.form['pass'],
                            'email' : request.form['email']
            })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash("Username already exist! Try again!")
    return render_template('register.html')
    
@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
                            categories=mongo.db.categories.find(),
                            images=mongo.db.images.find())
                            
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    meals =  mongo.db.meals
    meals.insert_one(request.form.to_dict())
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
@app.route('/recipe/<meal_id>', methods=['GET', 'POST'])
def recipe(meal_id):
    the_meal =  mongo.db.meals.find_one({"_id": ObjectId(meal_id)})
    return render_template('recipe.html', meals=the_meal)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)