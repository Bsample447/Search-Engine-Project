import sqlite3

class Database():
    def __init__(self):
        pass

    def connect(self):
        self.con = sqlite3.connect("data/websearch.db")
        self.cur = self.con.cursor()

    def close(self):
        self.con.commit()
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

    def import_blacklist(self):
        with open("data/blacklist.txt", 'r') as bl:
            _bl = bl.read().splitlines()

        self.connect()
        for i in _bl:
            try:
                self.cur.execute(f"insert into Blacklist(blacklist) values('{i}')")
                print(f'Adding {i} to blacklist')
            except Exception as e:
                print(f'{i} already exists in Blacklist')
        self.close()

    def create_schema(self):
        _schema_list = [["Keywords", "(keyword_id integer primary key, keyword varchar(64) unique)"],
                        ["URLs", "(url_id integer primary key, url text unique, description text unique)"],
                        ["Keywords_URLs", """(keyword_id integer, url_id integer,
                         foreign key(keyword_id) references Keywords(keyword_id),
                         foreign key(url_id) references URLs(urls_id))"""],
                        ["Blacklist", 
                         """(blacklist_id integer primary key, 
                         blacklist varchar(64) unique)"""]]

        for i in _schema_list:
            if self.exists(i[0]) == False:
                self.create_table(i[0], i[1])
                print(f'{i[0]} has been created')
            else:
                print(f'{i[0]} table already exists')

    def add(self, url, keywords, desc):
        self.connect()

        try:
            self.cur.execute(f"insert into URLs(url) values('{url}')")
            print(f'{url} added into URL table')
        except:
            print(f'{url} already exists in URL table')

        for keyword in keywords:
            try:
                self.cur.execute(f"insert into Keywords(keyword) values('{keyword}')")
                print(f'{keyword} added into Keyword table')
            except Exception as e:
                print(f'{keyword} already exists in Keyword table\n', e)

        self.close()
