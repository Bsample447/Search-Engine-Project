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

    def create_table(self, table, column):
        self.connect()
        s = f'''create table if not exists {table}{column}'''
        self.cur.execute(s)
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
                            unique (keyword_id, url_id))"""],
                        ["Crawled_URLs", """(
                            url_id integer unique,
                            foreign key (url_id) references URLs(url_id))"""]]

        for i in _schema_list:
            self.create_table(i[0], i[1])
            #print(f'{i[0]} has been created')

    def remember(self, urls):
        """Takes a list of URLs that are known but not necessarily crawled and adds them to the database of known URLs"""
        self.connect()

        self.cur.executemany("""insert or ignore 
                                  into URLs(url) 
                                  values(?)""", map(lambda url: (url,), urls))

        self.close()

    def nextUrl(self):
        """Compares the list of known URLs with the list of crawled URLs and returns the oldest uncrawled"""
        self.connect()

        self.cur.execute("select url from URLs where url_id not in (select url_id from Crawled_URLs) order by url_id limit 1")

        res = self.cur.fetchone()

        self.close()

        if res == None:
            return None
        else:
            return res[0]

    def linksCrawled(self):
        self.connect()

        self.cur.execute("select count(*) from Crawled_URLs")

        res = self.cur.fetchone()

        self.close()

        return res[0]

    def knownURLs(self):
        self.connect()

        self.cur.execute("select count(*) from URLs")

        res = self.cur.fetchone()

        self.close()

        return res[0]

    def add(self, url, keywords):
        self.connect()

        self.cur.execute(f"select url_id from urls where url = '{url}'")
        url_id = self.cur.fetchone()[0]

        self.cur.execute("insert or ignore into Crawled_URLs(url_id) values(?)", (url_id,))

        for keyword in keywords:
            self.cur.execute(f"""insert or ignore
                                   into Keywords(keyword) 
                                   values('{keyword}')""")

            self.cur.execute(f"select keyword_id from keywords where keyword = '{keyword}'")
            keyword_id = self.cur.fetchone()[0]

            self.cur.execute(f"""insert or ignore
                                   into Keywords_URLs (keyword_id, url_id)
                                   values ('{keyword_id}', '{url_id}')""")

        self.close()

    def crawled(self):
        self.connect()
        self.cur.execute(f"select url from URLs where url_id in (select url_id from Crawled_URLs)")
        url_list = []
        tmp = self.cur.fetchall()
        self.close()

        for url in tmp:
            url_list += [url[0]]

        return url_list

    def search(self, query):
        self.connect()

        req = ""
        for q in query:
            req += "'" + q + "', "
        req = req[:-2]
        s = f'''select url, cnt 
                 from URLs 
                 join (
                   select url_id, count(keyword_id) as cnt 
                     from Keywords_URLs 
                     where keyword_id in (
                       select keyword_id 
                         from keywords 
                         where keyword 
                           in ({req})) 
                         group by url_id order by cnt desc, url_id) as ks 
                           on URLs.url_id = ks.url_id limit 15'''

        self.connect()
        self.cur.execute(s)
        tmp = self.cur.fetchall()
        self.close()

        result = []
        for url in tmp:
            result += [url[0]]

        if result == None:
            result = []

        return result
