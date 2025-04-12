def save_selected_character(character_name):
    with open("selected_character.txt", "w") as file:
        file.write(character_name)

def load_selected_character():
    try:
        with open("selected_character.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "boy1"  # Default character if no file exists
