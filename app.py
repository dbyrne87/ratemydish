import os
import config
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'RateMyDish'
app.config["MONGO_URI"] = 'mongodb+srv://root:MyRootDataBase@myfirstcluster-ur0qm.mongodb.net/RateMyDish?retryWrites=true&w=majority'



mongo = PyMongo(app)


@app.route('/')
def meal_types():
    return render_template("test_connection.html", meals=mongo.db.meal_type.find())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)