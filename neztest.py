from modules import db

if __name__ == "__main__":
    db = db.Database()
    db.create_schema()
#    db.import_blacklist()

    # SYNTAX: db.add(URL, KEYWORD_LIST, DESCRIPTION)
    db.add('test.com', ['this', 'is', 'a', 'test'])
    db.add('test.com2', ['this2', 'is2', 'a2', 'test2'])
    db.add('test.com', ['this', 'is', 'a', 'test'])

    urls = db.crawled()
    print(urls)
