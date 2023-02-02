# Search engine algorithm
import requests

# sets app id and app key for API
# sign up at https://developer.edamam.com/edamam-recipe-api for id and key, and insert here
app_id = "47d553e8"
app_key = "b749a2fd18806cba1583c944bf24a546"

# defines variables to be used for including API parameters
includeAppId = "app_id={}".format(app_id)
includeAppKey = "app_key={}".format(app_key)

# asks user to enter ingredient(s)
ingredient = input("Enter one or more ingredients you want to use: ")
while ingredient == "":
    ingredient = input("You must enter at least one or more ingredients. Try again: ")
# use split and join functions to enable selection of more than one ingredient
ingredients = "q={}".format(ingredient)
# test
# print(ingredients)
url = 'https://api.edamam.com/auto-complete?{}&{}&{}'.format(ingredients, includeAppId, includeAppKey)
recipeChoices = 'You searched for ingredient options, using {} '.format(ingredients)

# requests and extracts recipes from the API, into the 'results' variable, based on user choices above
results = requests.get(url)
data = results.json()

# Printing the results
# prints 'You've searched for {cuisineReq}, {dietReq} recipes, using {ingredient(s)}'
# based on user's choices/input
print('================================================================================')
print(recipeChoices)
print(data)
