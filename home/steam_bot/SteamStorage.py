import sqlite3


class SteamStorage:
    def __init__(self, path: str):
        self.path = path
        self.conn = None
        self.cursor = None

    def init(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def fini(self):
        self.cursor.close()
        self.cursor = None
        self.conn.close()
        self.conn = None

    def create_table(self):
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS steam_service (
                uid INTEGER UNIQUE, 
                steam_id TEXT, 
                chat_id TEXT, 
                language_code TEXT, 
                enabled INTEGER
            ) """
        )

    def insert(self, uid, steam_id, chat_id, language_code):
        sql = """   INSERT INTO steam_service(uid, steam_id, chat_id, language_code, enabled) 
                    VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(sql, (uid, steam_id, chat_id, language_code, 1))
        self.conn.commit()

    def update_enabled(self, uid, enabled):
        sql = "UPDATE steam_service SET enabled=?  WHERE uid=?"
        self.cursor.execute(sql, (1 if enabled else 0, uid))
        self.conn.commit()

    def get(self, uid):
        sql = "SELECT * FROM steam_service WHERE uid=?"
        self.cursor.execute(sql, [uid])
        result = self.cursor.fetchone()
        return result

    def get_active(self):
        sql = "SELECT * FROM steam_service WHERE enabled=1"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def delete(self, uid):
        sql = "DELETE FROM steam_service WHERE uid=?"
        self.cursor.execute(sql, [uid])
