from modules import db
import crawler

if __name__ == "__main__":
    db = db.Database()
    db.create_schema()
    #crawler.web_crawl()

    query_input = ['brandon', 'is', 'a', 'roman', 'turd']
    result = db.search(query_input)

    for url in result:
        print(url)
