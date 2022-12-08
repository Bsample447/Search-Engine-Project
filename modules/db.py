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
        self.cur.execute(f"create table {table}{columns}")
        self.close()

    def create_schema(self):
        self.connect()
        
        _schema_list = [["Keywords", "(keyword_id int primary key, keyword varchar(64))"],
                        ["URLs", "(url_id int primary key, url text, last_update datetime)"],
                        ["Keywords_URLs", """(keyword_id int, url_id int,
                                              foreign key(keyword_Id) references Keywords(keyword_id),
                                              foreign key(url_id) references URLs(urls_id))"""],
                        ["Blacklist", "(blacklist_id int primary key, blacklist varchar(64))"],
                        ["Keywords_Blacklist", """(keyword_id int, blacklist_id int,
                                                   foreign key(keyword_id) references Keyword(keyword_id),
                                                   foreign key(blacklist_id) references Blacklist(blacklist_id))"""]]

        for i in _schema_list:
            if self.exists(i[0]) == False:
                self.create_table(i[0], i[1])
                print(f'{i[0]} has been created')
            else:
                print(f'{i[0]} table already exists')

        self.close()
