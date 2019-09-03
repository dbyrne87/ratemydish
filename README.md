# Code Institute Milestone Project - 3
## [RateMyDish](https://ratemydish.herokuapp.com/)
![Screenshot of website homepage](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/homepage.jpg?raw=true)
A website designed to allow users to easily users search or share recipes with the community, and benefit from having convenient access to recipes provided by all other members. 

This website can be used to find recipes by,
1.  Searching by recipe name or ingredient
2.  Picking From a list of Meal Types ie. Breakfast, Lunch, Dinner, Snack or Dessert
3.  Picking From a list of Cuisine Origins ie. French, Italian, Chinese etc.
4.  Picking From a list of Special Diet requirements ie. Vegitarian, Gluten-Free, Low-Fat etc.
5.  Picking From a list by Difficulty ie. Easy, Medium, Hard

### User Stories

- I don't know what I want for dinner today I want to search for something to make.
- I know exactly what I want to eat but I want to find a list of ingredients and the steps to make it.
- I want to find a meal that is suitable for me as I am gluten intolerent.  
-  My partner's favourite food is Chinese I want to search for a recipe to make for them that's easy to cook
-  I have to make the desserts for a get together what looks and tastes great that serves 6 people.
-  I don't know any good recipes for vegitarians. I want to find recipes that are highly rated by people who have made it already.
-  I think the meal I made is delicous I wonder would other people think the same?
## UX

Firstly a set of wireframe diagrams where made to show the layout of the website on different screen sizes and was also used to iron out any potential issues that arose before coding the website.[Link To Wireframe](https://www.lucidchart.com/invitations/accept/95406e85-8251-4772-b729-1a7cc6ec1470)

The websites layout is designed as simply and as user friendly as possible while allowing the user to easily navigate through the website to find, add, rate, modify or delete a recipe, the user can easily find the recipe they would like to find through a search field or from a small range of dropdowns.  

The design is based around the home.html page as the central part of the website, using this to easily lead the user to other pages using the Search functions or Most Liked / Favourites section , Log In/Out or Contact with the least amount of user unput. 

Using Bootstrap and CSS, depending on the users screen size, content is modified or removed (Such as the speech buuble on anything smaller than a Large screen) to make all the content easily read and interacted with.

The colour scheme throughout the website is kept as simple as possible and does not interfere with the usability or readability of the site. 
Using Modals in the homepage and dropdowns in the add/edit recipe pages information is available to the user when needed/wanted easily and is not overwhelming. 

If the client interacts with the website ie. Likes/Dislikes, Comments, Adds/Removes/Deletes a recipe they are informed using flash messages that the process was succesful or why it wasn't. An example of this would be if a "Guest" user tries to add a recipe. They will be brought directly to the log in page with a message explaining why they are there.  

## Features
![Website Home Page](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/homepage.jpg?raw=true)

If the user has already registered and logged in as a user they will be brought directly to the home page.
The home page has a large jumbotron image that is split in two allowing the user to easily see that they can 
a) Search for a Recipe using the Input field 
or 
b) Click on the buttons to easily find a range of recipes they are interested in using Bootstrap Modals. The values of the Meal Type, Cuisine Origin and Special Diet are each taken from a seperate collection from the Mongodb database. I set it up this way so that fields can be easily added or removed from the lists available to the user, without having to modify the html of multiple pages. 
Should the user not know what they want or are just browsing a range of Most Liked recipes or a set range of Favourites are available to choose from. 

The Navbar & Footer is kept the same throughout the site. If the user is logged in then a "Log Out" link is shown, otherwise a "Log In" link is shown. 
A User must be logged in to Add a recipe, if they are not and they click they are brought to the Log In/ Sign Up screen.
Any User is allowed in the Contact Us page but must add an email address to be allowed send a message. 
Social media links in the Footer allows all users, to see the websites social media accounts and keep up to date on new features, promoted places etc.  *no social media accounts are setup for this website at present and are for display only.

![Log In Page](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/log_in.jpg?raw=true)
Should the user be new to the site or not logged in then they will be brought directly to the Log In / Sign Up screen. 
The autoplay background video is only 8mb and is played in a loop so it should not effect load times a great deal. 
The page is broken down into 3 sections 
1)The Sign Up section has only 3 fields Username, Password & Email address. When the user signs up the site first checks if the username exists (if it does the site returns a message to the user explaining why) then it submits the data to the Users collection in Mongodb and redirects the user to the homepage.
2)The Log In section allows already registered users to access all the features of the website. On submitting the details it is checked against what's in the database and if it matches the user is directed to the homepage. If the username or password is incorrect the site returns a message explaining why the process was not succesful.
3)Should a user not want to sign up or log in they can click the Guest User button allowing them access to the site to search and view recipes only. Should these users attempt to Add or Modify a recipe then they will be redirected to the Log In screen again and asked to Sign Up or Log In. 

![Add Recipe Page](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/add_recipe.jpg?raw=true)
The Add recipe page allows users to add their own recipe for users to view and rate.
All fields are compulsery apart from the Image field which if left blank is given a default image as it is submitted. 
Dropdowns are heavily relied on so that data is kept uniform and allows for easy searching by other users. Fields such as prep time and cook time are only allowed numbers to keep data the same througout the database. 
Using Javascript/Jquery I added a dynamic field option to the Ingredients and Instructions section. This allows the user to only use the fields that they need. 
The first field in each section is mandatory and fields are limited to 10. If the user adds a field it becomes mandatory also and cannot be left blank meaning that only fields with data will be submitted to the database. 
After the submit the user is given a success flash message. 

![Edit Recipe Page](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/edit_recipe.jpg?raw=true)
The Edit Recipe page is very similar in appearance and function to the add recipe page allowing the user to easily update the recipe. All data in the database for the recipe is pre loaded/selected in the form meaning the user does not need to fill out the recipe fields again and can just update what they need. 
All 10 Ingrediant and Instruction fields are loaded so that all information can be easily viewed and modified. Any empty fields not needed can be deleted using the delete button before submitting the form. 
All previous likes/dislikes & comments the recipe has got before the edit are kept and are not lost in the edit. 
Only the owner of the recipe is allowed to Edit the Recipe, this is done by matching the logged in username data to the Chef name field. 
The delete recipe button is only available in the edit recipe page so that only the recipe owner can delete the recipe.

![Search Results Page](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/search_results.jpg?raw=true)
The Search Results page gives the results from any search made either through the search input field or the modal buttons. If the database has a recipe matching what was searched for it/they will be displayed in card form.
If nothing is returned the jumbotron search section is shown below a flash message asking the user to try a new search as no recipe was found. 

![Recipe Page Top](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/recipe_page_one.jpg?raw=true)
The Recipe Page displays all data in a clear manner. Each field is seperated and can easily be read and understood by the user. 
Large screens have a different layout to the medium and smaller sized screens. The Ingrediant and Instruction sections only display the steps that have values and are numbered to help follow the steps. 
![Recipe Page Middle](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/ratings.jpg?raw=true)
Next the Ratings section gets the current likes, dislikes and comments data from the database for the recipe and displays it to the user.
![Recipe Page Bottom](https://github.com/dbyrne87/ratemydish/blob/master/static/media/readme_images/have_your_say.jpg?raw=true)
The final section at the bottom of the page allows the user if they are signed in to like, dislike & comment on the recipe. After each click the page is refreshed with the new data and the user receives a success message. The Like and Dislike buttons are a different colour so that they do not blend in to the default colour scheme of the website. The Edit Recipe button can only be used by the owner of the recipe. 
  
##  Future Development
To develop the website even further given more time I would,

 - Limit the amount of clicks a registered user can like/dislike or comment on a recipe eg. one per recipe.
 - Display the persons username with an image who commented on the recipe.
 - Store the images if the recipes in the database and give the user the ability to upload an image also if they had it stored on their computer or mobile.
 - Allow the user to add a new Cuisine Origin or Special Diet option if they needed it.
 - In the python code develop a more elegent way (less lines of code) of inserting the edited Ingredient and Instruction data to the database. 
 
## Database Design
While designing the wireframes for the website and by researching other recipe websites, I wrote out all the data I wanted to collect from the user. 
I started by designing the Meal collection and listed all the keys it would need. 
I made a seperate collection for users and could link the two by the chef_name / username keys as I knew that they could not be duplicated in the site and so are unique. 
Even with a lot of planning the database did evolve as the site was being developed.
The Meal Type, Cuisine Type and Special Diet collections where added to the database so that it would be easier to add remove options  with the help of Jinja at a later date than trying to update multiple html dropdowns on multiple pages.
The origional plan was to store each comment in a seperate key/value in the meal collection but I decided it would be better to store them as an array an loop through them.

## Technologies Used
HTML5 & CSS3
Used for displaying the content and layout.

[Bootstrap](https://getbootstrap.com/)
Used to make the website clean and responsive.
Also used its built in features such as Modal and Alert fields.

[Javascript](https://www.javascript.com/)
Required for the dynamic fields in the Add and Edit recipe field functionality in the website in conjunction with jQuery.

[jQuery](http://code.jquery.com/)
Required for the dynamic fields in the Add and Edit recipe field functionality in the website in conjunction with jQuery.

[Python](https://www.python.org/)
Was used to write the logic of the site with the help of the Flask framework

[Flask](https://flask.palletsprojects.com/en/1.1.x/)
Flask was used as a micro framework on top of Python to develop the website quickly.

[MongoDb](https://www.mongodb.com/)
To store, manipulate and delete recipe and user data. 

[Jinja](http://jinja.pocoo.org/)
Used to display the data from the Flask app/ MongoDb to the user. 

[LucidChart](https://www.lucidchart.com/pages/home)
To Develop the Wireframes 

[Font Awesome](https://fontawesome.com/)
 To provide icons for the social media links, Website icon and button and tab icons.
 
[Google Fonts](https://fonts.google.com/)
 The website uses the "Sniglet" font throughout.  

## Testing
As the website was being built I used the built in features of [Cloud9](https://aws.amazon.com/cloud9/) and Google Chrome's built in developer tools. 

After each section was developed I,
1. made sure the content was responsive and laid out correctly as per the original wireframe on desktop, tablet and mobile devices using the Chrome developer tools.
2. made sure the code layout is correctly indented so it can be easily read. 
3. I used the [W3C Validator](https://validator.w3.org/), to make sure both the HTML and CSS was up to current standards and best practice. 
4. Check that data was displaying and upating correctly as I would expect.

### User scenarios:

 1. Land on a page,

		 Do you know what the website is for.
		 Is the page clear and user friendly. 
		 Do you know what to do to find what you are looking for easily?
 
 2.  Searching,
		
	     Is it clear what each type of search functionality does?
	   	 Do they do what is expected?
		 Are the results you received what you expected?
		
 3. Add/Edit/Delete Recipes,
 
	    Are the fields easy to understand.
        Is the layout of the page what you would typically expect?
        Does it feel overwhelming to add a recipe?
        Did you feel you had enough fields to add everything you wanted/needed to add
        If the recipe needed to be updated was this easy to do?
        If the recipe needed to be deleted was this easy to do?
        
		 
 4. Recipe Page
 
	    Was it what you expected?
        Was the page hard to understand follow or read?
        Did you have all the information you needed to make the recipe?


-   I tested the website on Chrome, Microsoft Edge and Firefox. I haven't found any issues so far.

### Real User Testing

When I felt the website was finished,
I asked friends and family to use the website and to give me feedback on issues they found or suggestions they had.

Some mentioned that on the recipe page the buttons where the same colour as the descriptive boxes making it hard to realise if they where a button or just text.
I changed the colour of these buttons to help them stand out. 
Some mentioned that the "No Comments Yet" in the comments section was still appearing after a comment has been added. This was happening due to pymongo removing the first "No Comments Field" it found in the database and not the specific recipe.  

### Bugs

Although it's not techically a bug I found it difficult to get around the "KeyError" message I was getting when updating the dynamic fields to the database. Anything I tried such as a "While" loop or "If" statement (without the try method) would give the error if one of the 10 fields was missing. Another way of doing it would be completly delete the recipe and re-upload the new data but I thought the try/else method worked better.    

## Heroku Deployment

Create a new app on heroku.com

Login to heroku with email and password from your Bash terminal
$ heroku login
Add heroku remote access from pop up or by clicking on link provided

$ heroku git:remote -a YOURAPPNAME

Add requirements.txt
$ sudo pip3 freeze --local > requirements.txt

Add Procfile 
$ echo web: python run.py > Procfile
Git commit and push to heroku remote

$ git add Procfile
$ git ci -m 'Add requirements.txt and Procfile'
$ git push -u heroku master

Set up dynos
$ heroku ps:scale web=1

Setup config variables on heroku dashboard such as SecretKey, IP and PORT

Your GitHub repo can be linked from the Heroku dashboard under the "Deploy" tab so that Heroku always has the latest commit running.

## Credits
Pretty Printed for helpful videos on setting up email and a user login in with Flask
(https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ)

Jquery Script .Net for the initial code used for the dynamic form fields
(https://www.jqueryscript.net/demo/Clone-Form-Sections-Subcomponents/)

UnSplash for the Jumbotron Image.
(https://unsplash.com/)

Pexels for the background Video and default recipe image
(https://www.pexels.com/)

MongodB documentation to help with explaining
$set operator
$inc operator
$regex
find_one_and_replace command
(https://docs.mongodb.com/manual/)

Stackoverflow for helping with 
Adding data to arrays
(https://stackoverflow.com/questions/46363485/pymongo-how-to-append-values-to-array?rq=1)
Explaining the Try Else Statements
(https://stackoverflow.com/questions/19522990/python-catch-exception-and-continue-try-block)
aswell as some more smaller issues I had

### Acknowledgements

Used W3C to check my HTML and CSS is correct and up to standard.
[W3C Validator](https://validator.w3.org/)

w3schools for refreshing my knowledge on simple coding challenges I faced that I haven't used in a while. 
https://www.w3schools.com/
