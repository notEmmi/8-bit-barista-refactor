import pygame



class GameState:
    def __init__(self, house="", pet="", name ="", selected_character="", fromPriorMenu=False, GameData=None):
        self.house = house
        self.pet = pet
        self.name = name
        self.selected_character = selected_character
        self.fromPriorMenu = fromPriorMenu
        self.GameData = GameData


    def save_to_db(self, conn):
        
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gamestate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                house TEXT,
                pet TEXT,
                name TEXT,
                selected_character TEXT,
                fromPriorMenu INTEGER,
                game_data TEXT
            )
        ''')
        cursor.execute('DELETE FROM gamestate')  # optional: only keep one saved state
        print(f"[DEBUG] Saving name to DB: {self.name}")
        print(f"[DEBUG] Saving character to DB: {self.selected_character}")
        cursor.execute('''
            INSERT INTO gamestate (house, pet, name, selected_character, fromPriorMenu, game_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.house,
            self.pet,
            self.name,
            self.selected_character,
            0,
            None,
            ))
        conn.commit()

    @classmethod
    def load_from_db(cls, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT house, pet, name, selected_character, fromPriorMenu, game_data FROM gamestate LIMIT 1')
        row = cursor.fetchone()
        if row:
            house, pet, name, selected_character, fromPriorMenu, game_data = row
            return cls(
                house=house,
                pet=pet,
                name=name,
                selected_character=selected_character,
                fromPriorMenu=bool(fromPriorMenu),
                GameData=game_data
            )
        else:
            return cls()  # return default if no saved state



    