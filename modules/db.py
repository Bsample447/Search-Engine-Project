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

    def create_schema(self):
        _schema_list = [["Keywords", """(
                           keyword_id integer primary key,
                           keyword varchar(64) unique)"""],
                        ["URLs", """(
                           url_id integer primary key,
                           url text unique)"""],
                        ["Keywords_URLs", """(
                            keyword_id integer,
                            url_id integer,
                            foreign key(keyword_id) references Keywords(keyword_id),
                            foreign key(url_id) references URLs(urls_id),
                            unique (keyword_id, url_id))"""]]

        for i in _schema_list:
            if self.exists(i[0]) == False:
                self.create_table(i[0], i[1])
                print(f'{i[0]} has been created')
            else:
                print(f'{i[0]} table already exists')

    def add(self, url, keywords):
        self.connect()

        self.cur.execute(f"""insert or ignore 
                               into URLs(url) 
                               values('{url}')""")

        for keyword in keywords:
            self.cur.execute(f"""insert or ignore
                                   into Keywords(keyword) 
                                   values('{keyword}')""")

            self.cur.execute(f"select url_id from urls where url = '{url}'")
            url_id = self.cur.fetchone()[0]

            self.cur.execute(f"select keyword_id from keywords where keyword = '{keyword}'")
            keyword_id = self.cur.fetchone()[0]

            self.cur.execute(f"""insert or ignore
                                   into Keywords_URLs (keyword_id, url_id)
                                   values ('{keyword_id}', '{url_id}')""")

        self.close()

    def crawled(self):
        self.connect()
        self.cur.execute(f"select url from URLs")
        url_list = []
        tmp = self.cur.fetchall()
        self.close()

        for url in tmp:
            url_list += [url[0]]

        return url_list
