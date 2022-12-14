from modules import db
import crawler

if __name__ == "__main__":
    db = db.Database()
    db.create_schema()
    #crawler.web_crawl()
    db.search(['roman', 'empire', 'war'])
