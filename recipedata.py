# items
theRecipes = {
    "Bagel": [("Wheat", 3), ("Water", 1)],
    "Croissant": [("Wheat", 2), ("Butter", 1)],
    "Muffin": [("Wheat", 3), ("Sugar", 3), ("Milk", 1)],
    "Coffee": [("Beans", 4), ("Milk", 1), ("Sugar", 1)],
    "Tea": [("Tea Leaves", 3), ("Water", 1)],
    "Smoothie": [("Banana", 1), ("Melon", 2), ("Milk", 1)],
}

def parseIngredients(ingredients: list) -> str:
    ingredientString = ""
    for ingredientAndAmount in ingredients:
        ingredientString = ingredientString + " " + str(ingredientAndAmount[1]) + "x " + ingredientAndAmount[0]
    return ingredientString[1:]

def getFirstTwoIngredients(ingredients: list) -> list:
    if (len(ingredients) < 2): return ingredients[0]
    return ingredients[0:2]