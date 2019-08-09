import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'RateMyDish'
app.config["MONGO_URI"] = 'mongodb+srv://root:MyRootDataBase@myfirstcluster-ur0qm.mongodb.net/RateMyDish?retryWrites=true&w=majority'



mongo = PyMongo(app)


@app.route('/')
def meal_types():
    return render_template("test_connection.html", 
    most_liked=mongo.db.meal_type.find(),
    favourites=mongo.db.meal_type.find(),
    meal_type_category=mongo.db.meal_type.find(),
    quisine_type_category=mongo.db.meal_type.find(),
    special_diet_type_category=mongo.db.meal_type.find(),
    difficulty_type_category=mongo.db.meal_type.find())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)