## RECIPE APP PROJECT FOR CFG PYTHON COURSE
## Recipe algorithm 
# imports requests module
import requests

# sets app id and app key for API
# sign up at https://developer.edamam.com/edamam-recipe-api for id and key, and insert here
app_id = "739875d8"
app_key = "d7176dfe27ce3cda845f772b28d7e106"

# sets out example input that will be accepted in the recipe selection criteria below
example_cuisineReq = ["American", "British", "Italian", "Mexican", "Indian", "Chinese"]
example_dietReq = ["vegetarian", "vegan", "alcohol-free", "gluten-free","pork-free"]

# defines variables to be used for including API parameters
includeAppId = "app_id={}".format(app_id)
includeAppKey = "app_key={}".format(app_key)
includeCuisineReq = ""
includeDietReq = ""

# asks user to enter ingredient(s)
ingredient = input("Enter one or more ingredients you want to use: ")
while ingredient == "":
    ingredient = input("You must enter at least one or more ingredients. Try again: ")
# use split and join functions to enable selection of more than one ingredient
components = ingredient.split()
items = ",+".join(components) or "and+".join(components) or " +".join(components)
ingredients = "ingredients=" + items
includeIngredients = "q={}".format(ingredients)
# test
# print(ingredients)

# asks user to enter cuisine preference (if any)
# (https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response)
cuisineReq = input(f"Choose your preferred cuisine from the following options, or type 'N' if none...\n{example_cuisineReq}: ")
while (cuisineReq != "N" and cuisineReq != "n") and (cuisineReq not in example_cuisineReq):
    cuisineReq = input(
        f"Invalid response. Choose your preferred cuisine from the following, or type 'N' if none...\n{example_cuisineReq}: ")
    cuisineReq_flag = 0
if cuisineReq == "N" or cuisineReq == "n":
    cuisineReq_flag = 0
elif cuisineReq in example_cuisineReq:
    includeCuisineReq = 'cuisineType={}'.format(cuisineReq)
    cuisineReq_flag = 1
# test
# print(includeCuisineReq)

# asks user to enter dietary requirements (if any)
# (https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response)
dietReq = input(f"Choose your dietary requirement(s) from the following options, or type 'N' if none...\n{example_dietReq}: ")
while (dietReq != "N" and dietReq != "n") and (dietReq not in example_dietReq):
    dietReq = input(
        f"Invalid response. Choose your dietary requirement from the following options, or type 'N' if none...\n{example_dietReq}: ")
    dietReq_flag = 0
if dietReq == 'N' or dietReq == 'n':
    dietReq_flag = 0
elif dietReq in example_dietReq:
    includeDietReq = 'health={}'.format(dietReq)
    dietReq_flag = 1
# test
# print(includeDietReq)

# asks user to enter maximum calorie preference
# (https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response)
# (https://stackoverflow.com/questions/5424716/how-to-check-if-string-input-is-a-number)
caloriesAsk = ""
while caloriesAsk is not int:
    try:
        caloriesReq = int(input("Enter the maximum number of calories per person: "))
        break
    except ValueError:
        print("Invalid response.")
# # test
# # print(caloriesReq)

# pulls API parameters into the url based on user choices, and sets relevant print message for each combo
if dietReq_flag == 1 and cuisineReq_flag == 1:
    url = 'https://api.edamam.com/search?{}&{}&{}&{}&{}'.format(includeIngredients, includeAppId, includeAppKey, includeDietReq, includeCuisineReq)
    recipeChoices = 'You searched for {} and {} recipe options, using {} '.format(cuisineReq, dietReq, components)
elif dietReq_flag == 0 and cuisineReq_flag == 1:
    url = 'https://api.edamam.com/search?{}&{}&{}&{}'.format(includeIngredients, includeAppId, includeAppKey, includeCuisineReq)
    recipeChoices = 'You searched for {} recipe options, using {} '.format(cuisineReq, components)
elif dietReq_flag == 1 and cuisineReq_flag == 0:
    url = 'https://api.edamam.com/search?{}&{}&{}&{}'.format(includeIngredients, includeAppId, includeAppKey, includeDietReq)
    recipeChoices = 'You searched for {} recipe options, using {} '.format(dietReq, components)
elif dietReq_flag == 0 and cuisineReq_flag == 0:
    url = 'https://api.edamam.com/search?{}&{}&{}'.format(includeIngredients, includeAppId, includeAppKey)
    recipeChoices = 'You searched for recipe options, using {} '.format(components)
# test whether the correct url is showing!
# print(url)
# print(recipeChoices)

# requests and extracts recipes from the API, into the 'results' variable, based on user choices above
results = requests.get(url)
data = results.json()
results = data['hits']

# Printing the results
# prints 'You've searched for {cuisineReq}, {dietReq} recipes, using {ingredient(s)}'
# based on user's choices/input
print('================================================================================')
print(recipeChoices)
# includes/prints calories preference
print(f'(under {caloriesReq} calories)')

# loops through results and adds 1 on each iteration (to count how many results found)
count = 0
for result in results:
    recipe = result['recipe']
    if int((recipe['calories']) / recipe['yield']) <= caloriesReq:
        count = count + 1
        
# if more than 0 results found, prints 'Here are your recipes'
if count > 0:
    print('Here are your recipes: ')
# else, if less than 0 results, prints 'Sorry, no recipes found' and the program ends here
else:
    print('================================================================================')
    print('Sorry, no recipes found!')
    
# loops through results again, where more than 0 results found...
for result in results:
    recipe = result['recipe']
    if int((recipe['calories']) / recipe['yield']) <= caloriesReq and count > 0:
        # define recipe info variables, i.e. name, web link, servings, nutrition, total time, and ingredients list
        recipeLabel = recipe['label']
        webLink = recipe['url']
        calories = round(int(recipe['calories'] / recipe['yield']))
        fat = recipe['totalNutrients']['FAT']
        fat_quantity = round(int(fat['quantity'] / recipe['yield']))
        protein = recipe['totalNutrients']['PROCNT']
        protein_quantity = round(int(protein['quantity'] / recipe['yield']))
        y = round(int(recipe['yield']))
        ingredList = recipe['ingredientLines']
        time = round(int(recipe['totalTime']))
        # prints recipe name, web link, servings, and nutrition info
        print('================================================================================')
        print(recipeLabel)
        print(webLink)
        print('Makes ' + str(y) + ' servings')
        print('Contains per serving: ' + str(calories) + ' calories, ' + str(fat_quantity) + 'g fat, ' + str(protein_quantity) + 'g protein')
        # not all recipes include total time, so prints this info only if they do (i.e. total time is more than 0 minutes)
        if time > 0:
            print('Total time: approximately ' + str(time) + ' minutes' )
        else:
            pass
    else:
        pass

# if more than one recipe found, asks user to choose a recipe and prints/saves shopping (ingredients) list to a text file
if count > 0:
    print('================================================================================')
    print('================================================================================')
    chosen_recipe = input('Which recipe do you want to cook? (Copy and paste the recipe as it is): ')
    if chosen_recipe == recipeLabel:
        MyFile=open('Shopping list.txt','w')
        MyFile.write(f'Shopping list: {recipeLabel} ({y} servings) ')
        MyFile.write('\n\n')
        for i in range(0, len(ingredList)):
            MyFile.write(ingredList[i])
            MyFile.write('\n')
        MyFile.write(f'\n(Link to recipe: {webLink})')
        MyFile.close()
        # prints final message to user, confirming shopping list file has been saved and asking if they want to open/print it
        print('================================================================================')
        print(f'Your shopping list for {recipeLabel} has been saved.\n')
        print_recipe = input('Would you like to print your shopping list? Y/N: ')
        print('\n')
        if print_recipe == 'Y' or print_recipe == 'y':
            with open('Shopping list.txt', 'r') as text_file:
                contents = text_file.read()
                print(contents)
        else:
            pass
        print('================================================================================')
        print('Happy cooking, and enjoy your meal!')
    else:
        pass
else:
    pass