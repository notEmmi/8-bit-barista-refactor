import pygame



class GameState:
    def __init__(self, house="", pet="", fromPriorMenu=False, GameData=None):
        self.house = house
        self.pet = pet
        self.fromPriorMenu = fromPriorMenu
        self.GameData = GameData


    def save_to_db(self, conn):
        
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gamestate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                house TEXT,
                pet TEXT,
                fromPriorMenu INTEGER,
                game_data TEXT
            )
        ''')
        cursor.execute('DELETE FROM gamestate')  # optional: only keep one saved state
        cursor.execute('''
            INSERT INTO gamestate (house, pet, fromPriorMenu, game_data)
            VALUES (?, ?, ?, ?)
        ''', (
            self.house,
            self.pet,
            0,
            None
            ))
        conn.commit()

    @classmethod
    def load_from_db(cls, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT house, pet, fromPriorMenu, game_data FROM gamestate LIMIT 1')
        row = cursor.fetchone()
        if row:
            house, pet, fromPriorMenu, game_data = row
            return cls(
                house=house,
                pet=pet,
                fromPriorMenu=bool(fromPriorMenu),
                GameData=game_data  # cast back if you need to parse JSON etc.
            )
        else:
            return cls()  # return default if no saved state



    