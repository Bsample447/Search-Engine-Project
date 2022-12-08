from modules import db

if __name__ == "__main__":
    db = db.Database()
    db.create_schema()
