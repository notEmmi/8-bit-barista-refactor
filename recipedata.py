# items
theRecipes = {
    "Bagel": [("Wheat", 3)],
    "Croissant": [("Wheat", 2), ("Butter", 1)],
    "Muffin": [("Wheat", 3), ("Sugar", 3), ("Milk", 1)],
    "Coffee": [("Beans", 4), ("Milk", 1), ("Sugar", 1), ("Cream", 1)],
    "Tea": [("Water", 1), ("Tea Leaves", 3)],
    "Smoothie": [("Water", 1), ("Banana", 1), ("Melon", 2)],
}

def parseIngredients(ingredients: list):
    ingredientString = ""
    for ingredientAndAmount in ingredients:
        ingredientString = ingredientString + " " + str(ingredientAndAmount[1]) + " " + ingredientAndAmount[0] + ","
    if (len(ingredientString) > 1): ingredientString = ingredientString[:-1] # remove trailing comma
    return ingredientString