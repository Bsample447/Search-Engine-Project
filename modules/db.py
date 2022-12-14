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
        _schema_list = [["Keywords", """(
                           keyword_id integer primary key,
                           keyword varchar(64) unique)"""],
                        ["URLs", """(
                           url_id integer primary key,
                           url text unique,
                           description text unique)"""],
                        ["Keywords_URLs", """(
                            keyword_id integer,
                            url_id integer,
                            foreign key(keyword_id) references Keywords(keyword_id),
                            foreign key(url_id) references URLs(urls_id),
                            unique (keyword_id, url_id))"""],
                        ["Blacklist", """(
                            blacklist_id integer primary key,
                            blacklist varchar(64) unique)"""],
                        ["Crawl", """(
                            crawl_id integer primary key,
                            crawl text unique)"""]]

        for i in _schema_list:
            if self.exists(i[0]) == False:
                self.create_table(i[0], i[1])
                print(f'{i[0]} has been created')
            else:
                print(f'{i[0]} table already exists')

    def add(self, url, keywords, desc):
        self.connect()

        self.cur.execute(f"""insert or ignore 
                               into URLs(url, description) 
                               values('{url}', '{desc}')""")

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

    def crawl(self, url = None):
        
        if url == None:
            self.connect()
            self.cur.execute(f"select crawl from Crawl")
            crawl_list = []
            tmp = self.cur.fetchall()
            self.close()

            for url in tmp:
                crawl_list += [url[0]]

            return crawl_list

        else:
            self.connect()
            self.cur.execute(f"""insert or ignore
                                   into Crawl(crawl)
                                   values ('{url}')""")
            self.close()
