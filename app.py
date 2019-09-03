#import modules and external file#
import os
import bcrypt
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId 
from flask_mail import Mail, Message
#from app_variables import *
from collections import OrderedDict

# Configure Flask and Mail Server #
app = Flask(__name__, static_url_path='/static')
app.config["MONGO_DBNAME"] = MONGO_DBNAME
app.config["MONGO_URI"] = MONGO_URI


app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_MAX_EMAILS'] = MAIL_MAX_EMAILS
app.config['MAIL_SUPRESS_SEND'] = MAIL_SUPRESS_SEND
app.config['MAIL_ASCII_ATTACHMENTS'] = MAIL_ASCII_ATTACHMENTS

mail = Mail(app)
mongo = PyMongo(app)

# Global Variables used multiple Times#
# Get Unique and Specific Data from each Key as used in home.html) #
meal_types_category = mongo.db.meal_types.distinct('meal_type')
cuisine_type_categories = mongo.db.cuisine_types.distinct('cuisine_types')
special_diet_type_category = mongo.db.special_diets.distinct('special_diet')
difficulty_type_category = mongo.db.meal_type.distinct('difficulty')


# Homepage will render home.html if user logged in or register.html if not #
@app.route('/')
def meal_types():
    # If the user is logged in #
    if 'username' in session:
        return render_template("home.html", 
        most_liked= mongo.db.meal_type.find(),
        favourites= mongo.db.meal_type.find(),
        meal_type_category= meal_types_category,
        cuisine_type_category= cuisine_type_categories,
        special_diet_type_category= special_diet_type_category,
        difficulty_type_category= difficulty_type_category,
        username= mongo.db.users.find_one({"username": session['username']}))
        
    # Else send them to the register.html page# 
    return render_template('register_login.html')


# Register Page, Has Sign Up (/register), Log In(/login) or Continue as Guest Options(/guest_login)#
@app.route('/register', methods=['POST', 'GET'])
def register():
    # Step 1: Check to see if username exists already #
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

    # Step 2: If Username doesn't exist add their details to the database and hash their password #
    if existing_user is None:
       hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
       users.insert({'name' : request.form['username'], 'password' : hashpass, 'email' : request.form['email']})
       session['username'] = request.form['username']
       return render_template("home.html", 
       most_liked=mongo.db.meal_type.find(),
       favourites=mongo.db.meal_type.find(),
       meal_type_category= meal_types_category,
       cuisine_type_category=cuisine_type_categories,
       special_diet_type_category=special_diet_type_category,
       difficulty_type_category=difficulty_type_category,
       username=mongo.db.users.find_one({"username": session['username']}))
    
    # Step 3: Else Return the user to register page with error #    
    return render_template('register_login.html',
    flash=flash('That Username is already taken please try again!'))    

# Register Page, Login section#
@app.route('/login', methods=['POST'])
def login():
    # Get the details the user has entered #
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    # If the username is in the database check the password and go to the homepage#
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
        # Else return to register screen with error if password incorrect#
        return render_template('register_login.html',
        flash=flash('Wrong Username and Password Combination. Please Try Again!'))
    # Else return to register screen with error if username incorrect#
    return render_template('register_login.html',
    flash=flash('Wrong Username and Password Combination. Please Try Again!'))   

@app.route('/guest_login')
def guest_login():
    # If User is already logged in #
    if 'username' in session:
        return render_template("home.html", 
        most_liked=mongo.db.meal_type.find(),
        favourites=mongo.db.meal_type.find(),
        meal_type_category=meal_types_category,
        cuisine_type_category=cuisine_type_categories,
        special_diet_type_category= special_diet_type_category,
        difficulty_type_category=difficulty_type_category,
        username=mongo.db.users.find_one({"username": session['username']}))
    
    # Else Render the same template as the above without a session cookie#
    return render_template("home.html", 
        most_liked=mongo.db.meal_type.find(),
        favourites=mongo.db.meal_type.find(),
        meal_type_category=meal_types_category,
        cuisine_type_category=cuisine_type_categories,
        special_diet_type_category= special_diet_type_category,
        difficulty_type_category=difficulty_type_category)    


# When a 'Get Recipe' button is clicked, it queries the database for the specific recipe details and returns it to the user in recipe_page.html #
@app.route('/view_recipe/<search>', methods=['POST', 'GET'])
def view_recipe(search):
    title_results =  mongo.db.meal_type.find_one( {'_id': ObjectId(request.form['get_recipe']) })
    if 'username' in session:
        return render_template('recipe_page.html', task=title_results,
        username=mongo.db.users.find_one({"username": session['username']}))
    return render_template('recipe_page.html', task=title_results)   

# If User is Logged In then allow them to add a Recipe #    
@app.route('/add_recipe')
def add_recipe():
    if 'username' in session:
        return render_template("add_recipe.html",
        meal_types= mongo.db.meal_types.find(), # Gets the values from the meal_types collection #
        cuisine_types= mongo.db.cuisine_types.find(), # Gets the values from the cuisine_types collection #
        special_diet= mongo.db.special_diets.find(), # Gets the values from the special_diets collection #                       
        username=mongo.db.users.find_one({"username": session['username']}))
# Else send them to the register page with message #        
    return render_template('register_login.html',
           flash=flash('You must Sign In to Add a Recipe!'))
    
# Function for inserting the recipe to the database #    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    meals=mongo.db.meal_type
    meals.insert_one(request.form.to_dict()) # inserts all the data to the database #
    # if the image_url wasn't entered give it a default value #
    mongo.db.meal_type.find_and_modify( {'image_url': ''}, update={"$set": {'image_url': 'https://images.pexels.com/photos/277253/pexels-photo-277253.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'}})
    # Modify the initial like & dislike values to a Integer and the comments value to an array #
    mongo.db.meal_type.find_and_modify( {'likes': '0'}, update={"$set": {'likes': 0 }})
    mongo.db.meal_type.find_and_modify( {'dislikes': '0'}, update={"$set": {'dislikes': 0 }})
    mongo.db.meal_type.find_and_modify( {'comments': ""}, update={"$set": {'comments': ['No Comments Yet'] }})
    return render_template('add_recipe.html', # Returns the user to the add_recipe page with success message #
            flash=flash('Your Recipe Has Been Added!'),
            meal_types= mongo.db.meal_types.find(), # Gets the values from the meal_types collection #
            cuisine_types= mongo.db.cuisine_types.find(), # Gets the values from the cuisine_types collection #
            special_diet= mongo.db.special_diets.find(), # Gets the values from the special_diets collection #                       
            username=mongo.db.users.find_one({"username": session['username']}))

# When Like Button is clicked it Increses Likes in the database of that recipe by 1 each time #
@app.route('/increase_recipe_likes', methods=['POST', 'GET'])
def increase_recipe_likes():
    if 'username' in session:
        mongo.db.meal_type.update( {"_id": ObjectId((request.form['increase_likes_button']))}, { "$inc": { "likes": 1 } } )#Increments by one on each click#
        the_task =  mongo.db.meal_type.find_one( {"_id": ObjectId((request.form['increase_likes_button']))} )
        return render_template('recipe_page.html', task=the_task,#Refreshes the current page with flash message and updated like#
        flash=flash('Thanks For Rating This Recipe!'),
        username=mongo.db.users.find_one({"username": session['username']}))
    return render_template('recipe_page.html', task=the_task, #Cannot like a recipe if not logged in#
    flash=flash('Sorry You must be logged in to Like a Recipe'))

    
# When Dislike Button is clicked it Increses Dislikes in the database of that recipe by 1 each time #    
@app.route('/increase_recipe_dislikes', methods=['POST', 'GET'])
def increase_recipe_dislikes():
    if 'username' in session:
        mongo.db.meal_type.update_one({'_id': ObjectId((request.form['increase_dislikes_button']))}, { "$inc": { "dislikes": 1 } })#Increments by one on each click#
        the_task =  mongo.db.meal_type.find_one( {"_id": ObjectId((request.form['increase_dislikes_button']))} )
        return render_template('recipe_page.html', task=the_task, #Refreshes the current page with flash message and updated dislike#
        flash=flash('Thanks For Rating This Recipe!'),
        username=mongo.db.users.find_one({"username": session['username']}))
    return render_template('recipe_page.html', task=the_task, #Cannot dislike a recipe if not logged in#
    flash=flash('Sorry You must be logged in to Dislike a Recipe'))

# If a comment is made it is added to the specific recipe as an array, further comments are added to this array.#
# If the comment key doesn't exist it is added#
@app.route('/add_comment/<search>', methods=['POST', 'GET'])
def add_comment(search):
    if 'username' in session:
        # if comments array is empty it removes the default 'No Comments Yet' before adding the new comment#
        recipe = mongo.db.meal_type.find_one( { '$and': [ {"_id": ObjectId((request.form['add_comment_button']))}, {'comments': ['No Comments Yet'] } ] })
        if recipe is not None:
            mongo.db.meal_type.update_one({'_id': ObjectId((request.form['add_comment_button']))}, { "$set": { "comments": [] } })
            add_this_comment = request.form['comment']# Get the comment from the form #
            mongo.db.meal_type.update( {"_id": ObjectId((request.form['add_comment_button']))}, { "$push": { "comments": add_this_comment }})# Add the new comment to the array #
            the_task =  mongo.db.meal_type.find_one( {"_id": ObjectId((request.form['add_comment_button']))} )
            return render_template('recipe_page.html', task=the_task,# Refreshes the page with flash message and updated comment#
            flash=flash('Thank You For Your Comment!'),
            username=mongo.db.users.find_one({"username": session['username']}))
        add_this_comment = request.form['comment']# Get the comment from the form #
        mongo.db.meal_type.update( {"_id": ObjectId((request.form['add_comment_button']))}, { "$push": { "comments": add_this_comment }})# Add the new comment to the array #
        the_task =  mongo.db.meal_type.find_one( {"_id": ObjectId((request.form['add_comment_button']))} )
        return render_template('recipe_page.html', task=the_task,# Refreshes the page with flash message and updated comment#
        flash=flash('Thank You For Your Comment!'),
        username=mongo.db.users.find_one({"username": session['username']}))    
    return render_template('recipe_page.html', task=the_task, #Cannot comment on a recipe if not logged in#
    flash=flash('Sorry You must be logged in to Dislike a Recipe'))
            

# Search the database for matching word/s in the Meal Title or Ingredients fields  #    
@app.route('/search', methods=['POST', 'GET'])
def search():
    search = request.form['search']# get value from the search input field#
    title_results =  mongo.db.meal_type.find( { '$or': [ {'meal_title': { '$regex': search,  '$options': 'i' }}, #searches for the word/s in all meal_title keys in the database#
        #searches for the word/s in all ingredients keys in the database#
        {'input_ingredients': { '$regex': search, '$options': 'i' }},
        {'Field2_input_ingredients': { '$regex': search,  '$options': 'i' }}, {'Field3_input_ingredients': { '$regex': search,  '$options': 'i' }},
        {'Field4_input_ingredients': { '$regex': search,  '$options': 'i' }}, {'Field5_input_ingredients': { '$regex': search,  '$options': 'i' }},
        {'Field6_input_ingredients': { '$regex': search,  '$options': 'i' }}, {'Field7_input_ingredients': { '$regex': search,  '$options': 'i' }},
        {'Field8_input_ingredients': { '$regex': search,  '$options': 'i' }}, {'Field9_input_ingredients': { '$regex': search,  '$options': 'i' }},
        {'Field10_input_ingredients': { '$regex': search,  '$options': 'i' }}] })
  
    #Filters out multiples of the same recipe being returned to the user ie. if 'cheese' is searched for and it is in the meal title and ingredients,#
    # it will only return the recipe once and not multiple times#
    unique = [] # Initially empty variable#
    for i in title_results:    
        if not i in unique:# If the recipe is not already in unique append it to unique#  
            unique.append(i)
    if 'username' in session:        
        return render_template('search_results.html', # Returns the list of results to the search_results page#
        meal_type_category= meal_types_category,
        cuisine_type_category= cuisine_type_categories,
        special_diet_type_category= special_diet_type_category,
        difficulty_type_category= difficulty_type_category,
        username=mongo.db.users.find_one({"username": session['username']}),
        task=unique)
    return render_template('search_results.html', # Returns the list of results to the search_results page#
    meal_type_category= meal_types_category,
    cuisine_type_category= cuisine_type_categories,
    special_diet_type_category= special_diet_type_category,
    difficulty_type_category= difficulty_type_category,
    task=unique)    

# Get's the _id of the recipe, queries the database for the specific recipe details, renders the edit_recipe.html page with the recipe data for updating #
@app.route('/edit_recipe/<search>', methods=['POST', 'GET'])
def edit_recipe(search):
    the_task =  mongo.db.meal_type.find_one({"_id": ObjectId((request.form['edit_button']))})
    all_categories =  mongo.db.meal_type.find()
    if 'username' in session:
        if session.get("username") == the_task.get("chef_name"): #Only the person who origionaly inputted the recipe can modify it#
            return render_template('edit_recipe.html', task=the_task,
            categories=all_categories,
            meal_types= mongo.db.meal_types.find(), # Gets the values from the meal_types collection #
            cuisine_types= mongo.db.cuisine_types.find(), # Gets the values from the cuisine_types collection #
            special_diet= mongo.db.special_diets.find(), # Gets the values from the special_diets collection #                       
            username=mongo.db.users.find_one({"username": session['username']}))
        return render_template("add_recipe.html", #If the user is not the chef it will bring them to the add_recipe page to add their own recipe#
        meal_types= mongo.db.meal_types.find(),
        cuisine_types= mongo.db.cuisine_types.find(),
        special_diet= mongo.db.special_diets.find(),
        flash=flash('You must be the Chef who Added The Recipe, please add your own recipe below!'),
        username=mongo.db.users.find_one({"username": session['username']})) 
    return render_template('register_login.html', # If the user is not logged in they will be brought to the register_login page to do so with a message explaining why#
    flash=flash('You Must be Logged In To Edit A Recipe!'))    
            
#Function to update recipe in database#
@app.route('/update_recipe', methods=['POST', 'GET']) 
def update_recipe():
    # Get the current ratings (likes/ dislikes/ comments and stores them in variables before they are deleted in the database) #
    ratings = mongo.db.meal_type.find_one({"_id": ObjectId((request.form['recipe_update-button']))})
    likes_count = ratings.get('likes')
    dislikes_count = ratings.get('dislikes')
    comments_count = ratings.get('comments')
    # Replace the recipe with id in the form with this new data, completely wipes all origional data so current likes/dislike & comments are added form the variables and not the form#
    mongo.db.meal_type.find_one_and_replace( {"_id": ObjectId((request.form['recipe_update-button']))},
        {"meal_title": (request.form['meal_title']), "chef_name": (request.form['chef_name']),
            "meal_type": (request.form['meal_type']), "difficulty": (request.form['difficulty']),
            "prep_time": (request.form['prep_time']), "cook_time": (request.form['cook_time']),
            "servings": (request.form['servings']), "calories": (request.form['calories']),
            "special_diet": (request.form['special_diet']), "image_url": (request.form['image_url']),
            "likes": likes_count, "dislikes": dislikes_count, "cuisine_type": (request.form['cuisine_type']),
            "comments": comments_count, "input_ingredients": (request.form['input_ingredients']),
            "input_instructions": (request.form['input_instructions'])
        })
    # Input Ingredients #
    # Finds the current amount of fields used in the edit_recipe form and adds only the amount of fields needed with the updated data#
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field10_input_ingredients']): 
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients']), "Field5_input_ingredients": (request.form['Field5_input_ingredients']),
                    "Field6_input_ingredients": (request.form['Field6_input_ingredients']), "Field7_input_ingredients": (request.form['Field7_input_ingredients']),
                    "Field8_input_ingredients": (request.form['Field8_input_ingredients']), "Field9_input_ingredients": (request.form['Field9_input_ingredients']),
                    "Field10_input_ingredients": (request.form['Field10_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field9_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients']), "Field5_input_ingredients": (request.form['Field5_input_ingredients']),
                    "Field6_input_ingredients": (request.form['Field6_input_ingredients']), "Field7_input_ingredients": (request.form['Field7_input_ingredients']),
                    "Field8_input_ingredients": (request.form['Field8_input_ingredients']), "Field9_input_ingredients": (request.form['Field9_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field8_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients']), "Field5_input_ingredients": (request.form['Field5_input_ingredients']),
                    "Field6_input_ingredients": (request.form['Field6_input_ingredients']), "Field7_input_ingredients": (request.form['Field7_input_ingredients']),
                    "Field8_input_ingredients": (request.form['Field8_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field7_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients']), "Field5_input_ingredients": (request.form['Field5_input_ingredients']),
                    "Field6_input_ingredients": (request.form['Field6_input_ingredients']), "Field7_input_ingredients": (request.form['Field7_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field6_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients']), "Field5_input_ingredients": (request.form['Field5_input_ingredients']),
                    "Field6_input_ingredients": (request.form['Field6_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field5_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients']), "Field5_input_ingredients": (request.form['Field5_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field4_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients']),
                    "Field4_input_ingredients": (request.form['Field4_input_ingredients'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field3_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients']), "Field3_input_ingredients": (request.form['Field3_input_ingredients'])
                }})
    except KeyError:
        pass                                        
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['Field2_input_ingredients']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"Field2_input_ingredients": (request.form['Field2_input_ingredients'])
                }})
    except KeyError:
        pass
   
   
    # Input Instructions #
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['ID10_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions']), "ID5_input_instructions": (request.form['ID5_input_instructions']),
                    "ID6_input_instructions": (request.form['ID6_input_instructions']), "ID7_input_instructions": (request.form['ID7_input_instructions']),
                    "ID8_input_instructions": (request.form['ID8_input_instructions']), "ID9_input_instructions": (request.form['ID9_input_instructions']),
                    "ID10_input_instructions": (request.form['ID10_input_instructions'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#    
        if (request.form['ID9_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))}, 
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions']), "ID5_input_instructions": (request.form['ID5_input_instructions']),
                    "ID6_input_instructions": (request.form['ID6_input_instructions']), "ID7_input_instructions": (request.form['ID7_input_instructions']),
                    "ID8_input_instructions": (request.form['ID8_input_instructions']), "ID9_input_instructions": (request.form['ID9_input_instructions'])
                }})
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['ID8_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions']), "ID5_input_instructions": (request.form['ID5_input_instructions']),
                    "ID6_input_instructions": (request.form['ID6_input_instructions']), "ID7_input_instructions": (request.form['ID7_input_instructions']),
                    "ID8_input_instructions": (request.form['ID8_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#    
        if (request.form['ID7_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions']), "ID5_input_instructions": (request.form['ID5_input_instructions']),
                    "ID6_input_instructions": (request.form['ID6_input_instructions']), "ID7_input_instructions": (request.form['ID7_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['ID6_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions']), "ID5_input_instructions": (request.form['ID5_input_instructions']),
                    "ID6_input_instructions": (request.form['ID6_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['ID5_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions']), "ID5_input_instructions": (request.form['ID5_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['ID4_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions']),
                    "ID4_input_instructions": (request.form['ID4_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form# 
        if (request.form['ID3_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions']), "ID3_input_instructions": (request.form['ID3_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    try: # if this field exists in the form do the below if not don't give an error but try the next #
    # Only calls the database when it finds the highest numbered field in the form#
        if (request.form['ID2_input_instructions']):
            mongo.db.meal_type.find_one_and_update( {"_id": ObjectId((request.form['recipe_update-button']))},
                { "$set":  
                    {"ID2_input_instructions": (request.form['ID2_input_instructions'])
                }}) 
    except KeyError:
        pass
    
    # If the image_url is empty or has been removed then update it to the default value #
    mongo.db.meal_type.find_and_modify( {'image_url': ''}, update={"$set": {'image_url': 'https://images.pexels.com/photos/1268558/pexels-photo-1268558.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'}})
    return render_template("home.html", 
    most_liked=mongo.db.meal_type.find(),
    favourites=mongo.db.meal_type.find(),
    meal_type_category=meal_types_category,
    cuisine_type_category=cuisine_type_categories,
    special_diet_type_category= special_diet_type_category,
    difficulty_type_category=difficulty_type_category,
    username=mongo.db.users.find_one({"username": session['username']}))

# Function for deleting Recipe. Can only be accessed from the edit_recipe page so only available to the recipe owner#            
@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    mongo.db.meal_type.remove({'_id': ObjectId((request.form['recipe_delete-button']))})
    return render_template("home.html", 
    most_liked=mongo.db.meal_type.find(),
    favourites=mongo.db.meal_type.find(),
    meal_type_category=meal_types_category,
    cuisine_type_category=cuisine_type_categories,
    special_diet_type_category= special_diet_type_category,
    difficulty_type_category=difficulty_type_category,
    flash=flash('The Recipe Has Been Deleted!'),
    username=mongo.db.users.find_one({"username": session['username']}))


# If Logout Button is clicked then it removes the session cookie and brings them to the register page with message #
@app.route('/logout')
def logout():
    session.clear()
    return render_template('register_login.html',
        flash=flash('You have been Signed Out!'))

# Modal buttons on Hompage, #
# Queries database and shows in Modal the list of that particlular Key #
# When value in modal is choosen it will display a list of recipes that contain that value if they exist#
@app.route('/category_results', methods=['POST', 'GET'])
def category_results():
    if request.form['type_category_button'] in ('Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Snack'):
        category_results=mongo.db.meal_type.find({'meal_type': request.form['type_category_button']})
        if 'username' in session:
            return render_template('search_results.html',
            meal_type_category= meal_types_category,
            cuisine_type_category=cuisine_type_categories,
            special_diet_type_category=special_diet_type_category,
            difficulty_type_category=difficulty_type_category,
            username=mongo.db.users.find_one({"username": session['username']}),
            task=category_results)
        return render_template('search_results.html',
        meal_type_category= meal_types_category,
        cuisine_type_category=cuisine_type_categories,
        special_diet_type_category=special_diet_type_category,
        difficulty_type_category=difficulty_type_category,
        task=category_results)
        
        # Complete list of Cuisine Origins if they are not in any recipe in the database then they will not be shown to the user #
    elif request.form['type_category_button'] in ('American', 'Chinese', 'French', 'Greek', 'Indian', 'Irish', 'Italian', 'Mexican', 'Thai', 'Turkish', 'Other'):
         category_results=mongo.db.meal_type.find({'cuisine_type': request.form['type_category_button']})
         if 'username' in session:
            return render_template('search_results.html',
            meal_type_category= meal_types_category,
            cuisine_type_category=cuisine_type_categories,
            special_diet_type_category=special_diet_type_category,
            difficulty_type_category=difficulty_type_category,
            username=mongo.db.users.find_one({"username": session['username']}),
            task=category_results)
         return render_template('search_results.html',
         meal_type_category= meal_types_category,
         cuisine_type_category=cuisine_type_categories,
         special_diet_type_category=special_diet_type_category,
         difficulty_type_category=difficulty_type_category,
         task=category_results)
                 # Complete list of Special Diets if they are not in any recipe in the database then they will not be shown to the user #
    elif request.form['type_category_button'] in ('Vegetarian', 'Vegan', 'Weight Watchers', 'Gluten-free', 'Ketogenic', 'High-protein', 'Low Fat', 'Low-Carb', 'Other Diet', 'Not Applicable'):
         category_results=mongo.db.meal_type.find({'special_diet': request.form['type_category_button']})
         if 'username' in session:
            return render_template('search_results.html',
            meal_type_category= meal_types_category,
            cuisine_type_category=cuisine_type_categories,
            special_diet_type_category=special_diet_type_category,
            difficulty_type_category=difficulty_type_category,
            username=mongo.db.users.find_one({"username": session['username']}),
            task=category_results)
         return render_template('search_results.html',
         meal_type_category= meal_types_category,
         cuisine_type_category=cuisine_type_categories,
         special_diet_type_category=special_diet_type_category,
         difficulty_type_category=difficulty_type_category,
         task=category_results)
         
    elif request.form['type_category_button'] in ('Easy', 'Medium', 'Hard'):
         category_results=mongo.db.meal_type.find({'difficulty': request.form['type_category_button']})
         if 'username' in session:
            return render_template('search_results.html',
            meal_type_category= meal_types_category,
            cuisine_type_category=cuisine_type_categories,
            special_diet_type_category=special_diet_type_category,
            difficulty_type_category=difficulty_type_category,
            username=mongo.db.users.find_one({"username": session['username']}),
            task=category_results)
         return render_template('search_results.html',
         meal_type_category= meal_types_category,
         cuisine_type_category=cuisine_type_categories,
         special_diet_type_category=special_diet_type_category,
         difficulty_type_category=difficulty_type_category,
         task=category_results)     


# Contact Us Form and Function for Sending the email#
@app.route('/contact_us', methods=['POST', 'GET'])
def contact_us():
    return render_template('contact_us.html')

@app.route('/send_email', methods=['POST', 'GET'])
def send_email():
    email = Message('You Have Mail', recipients=[MAIL_RECIPIENT])
    msg_name = request.form['name']
    msg_email = request.form['email_address']
    msg_message = request.form['message']
    email.html = 'From:'+ msg_name + '<br> Email:'+ msg_email + '<br> Message: <br>' + msg_message
    
    mail.send(email)
    return render_template('contact_us.html',
    flash= flash('Your Email Has been Sent!'))

#Settings For Running Locally#
#if __name__ == '__main__':
    #app.secret_key = SECRET_KEY
  #  app.run(host=HOST, port=PORT, debug=DEBUG)

#Settings for Running on Heroku #    
if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
            debug=False)