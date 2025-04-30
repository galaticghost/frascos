import psycopg
from psycopg.rows import dict_row

class Database():
    conn = psycopg.connect("dbname=frascos user=frascos_db password=postgres port=5432 host=localhost", row_factory=dict_row)
    cur = conn.cursor()

    def select_user(self,campo,data): # TODO
        result = self.cur.execute(f"SELECT id,username,email,password,profile_picture,last_seen,about_me FROM users WHERE {campo} = %s ;",
                            (data,)).fetchone()
        return result
        
        
        
        
