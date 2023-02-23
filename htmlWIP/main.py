from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests
import json
import csv

#more than likely need to pip install flask
# and pip install

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/htmlWIP/ - the following will be our login page, which will use both GET and POST requests
@app.route('/htmlWIP/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        if verify_login(username, password):
            msg = 'Logged in Successfully!'
            session['loggedin'] = True
            session['username'] = username
            session['password'] = password
            return redirect(url_for('search'))
        else:
            msg = 'Username or password is Incorrect!'
    #Show the login form with message (if any)
    return render_template('index.html', msg='')

def verify_login(username, password):
    with open('CSVFolder/userinfo.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader) #Skips header
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/htmlWIP/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

def create_user(username, password):
    with open('CSVFolder/userinfo.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return False
    with open('CSVFolder/userinfo.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    return True

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/htmlWIP/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password2' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if password  == password2:
            if not username or not password:
                return 'Username and password are required'
            if create_user(username, password):
                return 'User created successfully'
            else:
                return 'User already exists'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/htmlWIP/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('search.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/htmlWIP/main')
def main():
    # Output message if something goes wrong...
    msg = ''
    if 'loggedin' in session:
        #Show the login form with message (if any)
        username = session['username']
        password = session['password']
        return render_template('main.html',accUser = username, accPass = password,msg='')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/htmlWIP/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        username = session['username']
        password = session['password']
        verify_login(username, password)
        account = (username, password)
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/htmlWIP/search', methods=['GET','POST'])
def search():
    if 'loggedin' in session:
        # sets app id and app key for API
        # sign up at https://developer.edamam.com/edamam-recipe-api for id and key, and insert here
        app_id = "47d553e8"
        app_key = "b749a2fd18806cba1583c944bf24a546"
        result=''
        # defines variables to be used for including API parameters
        includeAppId = "app_id={}".format(app_id)
        includeAppKey = "app_key={}".format(app_key)

            # POST request
        if request.method == 'POST' and 'search' in request.form:
            # asks user to enter ingredient(s)
            ingredient = request.form['search']
            while ingredient == "":
                ingredient = input("You must enter at least one or more ingredients. Try again: ")
            # use split and join functions to enable selection of more than one ingredient
            ingredients = "q={}".format(ingredient)
            # test
            # print(ingredients)
            url = 'https://api.edamam.com/auto-complete?{}&{}&{}'.format(ingredients, includeAppId, includeAppKey)
            #recipeChoices = 'You searched for ingredient options, using {} '.format(ingredients)

            # requests and extracts recipes from the API, into the 'results' variable, based on user choices above
            results = requests.get(url)
            datas = json.loads(results.text)
            data_list = []
            for data in datas:
                print(data)
                data_list.append(data)


            # Printing the results
            # prints 'You've searched for {cuisineReq}, {dietReq} recipes, using {ingredient(s)}'
            # based on user's choices/input
            result = data_list
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            result = 'Please fill out the form!'
        return render_template('search.html', result = result)
    return redirect(url_for('login'))

@app.route('/htmlWIP/recipesearch', methods=['GET','POST'])
def recipesearch():
    if 'loggedin' in session:
        app_id = "739875d8"
        app_key = "d7176dfe27ce3cda845f772b28d7e106"
        username = session['username']
        recipe=''
        # defines variables to be used for including API parameters
        includeAppId = "app_id={}".format(app_id)
        includeAppKey = "app_key={}".format(app_key)

        ingredient = request.cookies.get('ingredients')

        # use split and join functions to enable selection of more than one ingredient
        components = ingredient.split()
        items = ",+".join(components) or "and+".join(components) or " +".join(components)
        ingredients = "ingredients=" + items
        includeIngredients = "q={}".format(ingredients)
        # test
        # print(ingredients)
        url = 'https://api.edamam.com/search?{}&{}&{}'.format(includeIngredients, includeAppId, includeAppKey)
        #recipeChoices = 'You searched for ingredient options, using {} '.format(ingredients)

        # requests and extracts recipes from the API, into the 'results' variable, based on user choices above
        results = requests.get(url)
        datas = results.json()
        results = datas['hits']

        # loops through results and adds 1 on each iteration (to count how many results found)
        count = 0
        for result in results:
            recipe = result['recipe']
            if int((recipe['calories']) / recipe['yield']):
                count = count + 1
            
        # if more than 0 results found, prints 'Here are your recipes'
        if count > 0:
            print('Here are your recipes: ')
        # else, if less than 0 results, prints 'Sorry, no recipes found' and the program ends here
        else:
            print('================================================================================')
            print('Sorry, no recipes found!')
        recipeList = []   
        linkList = []
        # loops through results again, where more than 0 results found...
        with open('CSVFolder/searchitems.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for result in results:
                recipe = result['recipe']
                if int((recipe['calories']) / recipe['yield']) and count > 0:
                    # define recipe info variables, i.e. name, web link, servings, nutrition, total time, and ingredients list
                    recipeLabel = recipe['label']
                    webLink = recipe['url']
                    calories = round(int(recipe['calories'] / recipe['yield']))
                    fat = recipe['totalNutrients']['FAT']
                    fat_quantity = round(int(fat['quantity'] / recipe['yield']))
                    protein = recipe['totalNutrients']['PROCNT']
                    protein_quantity = round(int(protein['quantity'] / recipe['yield']))
                    y = round(int(recipe['yield']))
                    time = round(int(recipe['totalTime']))
                    # prints recipe name, web link, servings, and nutrition info
                    recipeList.append(recipeLabel)
                    linkList.append(webLink)
                    writer.writerow([username,recipeLabel, webLink, str(calories),str(fat_quantity),str(protein_quantity),str(y),str(time)])
                else:
                    pass         
        return render_template('search.html', result2 = recipeList, result3 = linkList, len = len(recipeList))
    return redirect(url_for('login'))
   


