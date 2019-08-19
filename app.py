import os
import bcrypt
import numpy as np 
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'RateMyDish'
app.config["MONGO_URI"] = 'mongodb+srv://root:MyRootDataBase@myfirstcluster-ur0qm.mongodb.net/RateMyDish?retryWrites=true&w=majority'



mongo = PyMongo(app)

@app.route('/')
def meal_types():
    meal_types_category = mongo.db.meal_type.distinct('meal_type')
    cuisine_type_categories = mongo.db.meal_type.distinct('cuisine_type')
    special_diet_type_category = mongo.db.meal_type.distinct('special_diet')
    difficulty_type_category = mongo.db.meal_type.distinct('difficulty')
    if 'username' in session:
        return render_template("home.html", 
        most_liked=mongo.db.meal_type.find(),
        favourites=mongo.db.meal_type.find(),
        meal_type_category= meal_types_category,
        cuisine_type_category=cuisine_type_categories,
        special_diet_type_category=special_diet_type_category,
        difficulty_type_category=difficulty_type_category,
        username=mongo.db.users.find_one({"username": session['username']}))
        
     
    return render_template('register_login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

    if existing_user is None:
       hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
       users.insert({'name' : request.form['username'], 'password' : hashpass, 'email' : request.form['email']})
       session['username'] = request.form['username']
       return render_template("home.html", 
       most_liked=mongo.db.meal_type.find(),
       favourites=mongo.db.meal_type.find(),
       meal_type_category=mongo.db.meal_type.find(),
       cuisine_type_category=mongo.db.meal_type.find(),
       special_diet_type_category=mongo.db.meal_type.find(),
       difficulty_type_category=mongo.db.meal_type.find(),
       username=mongo.db.users.find_one({"username": session['username']}))
        
    return render_template('register_login.html',
    flash=flash('That Username is already taken please try again!'))    

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    meal_types_category = mongo.db.meal_type.distinct('meal_type')
    cuisine_type_categories = mongo.db.meal_type.distinct('cuisine_type')
    special_diet_type_category = mongo.db.meal_type.distinct('special_diet')
    difficulty_type_category = mongo.db.meal_type.distinct('difficulty')

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']: 
            session['username'] = request.form['username']
            return render_template("home.html", 
            most_liked=mongo.db.meal_type.find(),
            favourites=mongo.db.meal_type.find(),
            meal_type_category= meal_types_category,
            cuisine_type_category=cuisine_type_categories,
            special_diet_type_category=special_diet_type_category,
            difficulty_type_category=difficulty_type_category,
            username=mongo.db.users.find_one({"username": session['username']}))

        return render_template('register_login.html',
        flash=flash('Wrong Username and Password Combination. Please Try Again!'))

    return render_template("home.html", 
    most_liked=mongo.db.meal_type.find(),
    favourites=mongo.db.meal_type.find(),
    meal_type_category=mongo.db.meal_type.find(),
    cuisine_type_category=mongo.db.meal_type.find(),
    special_diet_type_category=mongo.db.meal_type.find(),
    difficulty_type_category=mongo.db.meal_type.find(),
    username=mongo.db.users.find_one({"username": session['username']}))   

@app.route('/guest_login')
def guest_login():
    meal_types_category = mongo.db.meal_type.distinct('meal_type')
    cuisine_type_categories = mongo.db.meal_type.distinct('cuisine_type')
    special_diet_type_category = mongo.db.meal_type.distinct('special_diet')
    difficulty_type_category = mongo.db.meal_type.distinct('difficulty')
    
    if 'username' in session:
        return render_template("home.html", 
        most_liked=mongo.db.meal_type.find(),
        favourites=mongo.db.meal_type.find(),
        meal_type_category=meal_types_category,
        cuisine_type_category=cuisine_type_categories,
        special_diet_type_category= special_diet_type_category,
        difficulty_type_category=difficulty_type_category,
        username=mongo.db.users.find_one({"username": session['username']}))
    
    return render_template("home.html", 
        most_liked=mongo.db.meal_type.find(),
        favourites=mongo.db.meal_type.find(),
        meal_type_category=meal_types_category,
        cuisine_type_category=cuisine_type_categories,
        special_diet_type_category= special_diet_type_category,
        difficulty_type_category=difficulty_type_category)    

@app.route('/contact_us', methods=['POST', 'GET'])
def contact_us():
    return render_template('contact_us.html')

@app.route('/view_recipe/<search>', methods=['POST', 'GET'])
def view_recipe(search):
    title_results =  mongo.db.meal_type.find_one( {'_id': ObjectId(request.form['get_recipe']) })
    return render_template('recipepage.html', task=title_results,
    username=mongo.db.users.find_one({"username": session['username']})) 

@app.route('/edit_test')
def edit_test():
    return render_template("editbuttontest.html",
    meal_type_category=mongo.db.meal_type.find())

@app.route('/edit_recipe/<meal_type>')
def edit_recipe(meal_type):
    the_task =  mongo.db.meal_type.find_one({"_id": ObjectId(meal_type)})
    all_categories =  mongo.db.meal_type.find()
    return render_template('editrecipe.html', task=the_task,
                           categories=all_categories,
    username=mongo.db.users.find_one({"username": session['username']}))  
    
@app.route('/search', methods=['POST', 'GET'])
def search():
    search = request.form['search']
    title_results =  mongo.db.meal_type.find( { '$or': [ {'meal_title': { '$regex': search,  '$options': 'i' }}, 
                                              {'email_address': { '$regex': search, '$options': 'i' }} ] })
    return render_template('searchtest.html', task=title_results)
    
@app.route('/add_recipe')
def add_recipe():
    if 'username' in session:
        return render_template("addrecipe.html",
        username=mongo.db.users.find_one({"username": session['username']}))
        
    return render_template('register_login.html',
           flash=flash('You must Sign In to Add a Recipe!'))
    
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    meals=mongo.db.meal_type
    meals.insert_one.lower(request.form.to_dict())
    return render_template('addrecipe.html',
           flash=flash('Your Recipe Has Been Added!'),
           username=mongo.db.users.find_one({"username": session['username']}))
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('register_login.html',
        flash=flash('You have been Signed Out!'))
        
@app.route('/category_results', methods=['POST', 'GET'])
def category_results():
    if request.form['type_category_button'] in ('Breakfast', 'Lunch', 'Dinner', 'Snack'):
        category_results=mongo.db.meal_type.find({'meal_type': request.form['type_category_button']})
        return render_template('category_results.html', tasks=category_results)
    elif request.form['type_category_button'] in ('American', 'Chinese', 'French', 'Greek', 'Indian', 'Irish', 'Italian', 'Mexican', 'Thai', 'Turkish', 'Other'):
         category_results=mongo.db.meal_type.find({'cuisine_type': request.form['type_category_button']})
         return render_template('category_results.html', tasks=category_results)
    elif request.form['type_category_button'] in ('Vegetarian', 'Vegan', 'Weight Watchers', 'Gluten-free', 'Ketogenic', 'High-protein', 'Low Fat', 'Low-Carb', 'Other Diet'):
         category_results=mongo.db.meal_type.find({'special_diet': request.form['type_category_button']})
         return render_template('category_results.html', tasks=category_results)
    elif request.form['type_category_button'] in ('Easy', 'Medium', 'Hard'):
         category_results=mongo.db.meal_type.find({'difficulty': request.form['type_category_button']})
         return render_template('category_results.html', tasks=category_results)     
       

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=8080, debug=True)
    
    