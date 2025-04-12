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



    