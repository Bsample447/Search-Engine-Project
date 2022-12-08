import sqlite3

class Database():
    def __init__(self):
        pass

    def connect(self):
        self.con = sqlite3.connect("data/websearch.db")
        self.cur = self.con.cursor()

    def close(self):
        self.con.close()

    def exists(self, table = "Keywords"):
        self.connect()
        self.cur.execute(f"select count(Name) from sqlite_master where type='table' and name='{table}'")
        
        if self.cur.fetchone()[0]==1:
            return True
        else:
            return False

        self.close()

    def create_table(self, table, columns):
        self.connect()
        self.cur.execute(f"""create table {table} {columns}""")
        self.close()

    def create_schema(self):
        self.connect()
        
        if self.exists("Keywords") == False:
            self.create_table("Keywords",
                              """(keyword_id int primary key,
                                 keyword varchar(64))""")
        else:
            print('Keywords table already exists')
        self.close()
