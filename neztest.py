from modules import db

if __name__ == "__main__":
    db = db.Database()
    result = db.exists("Keywords")
    print(result)

    db.create_schema()

    result = db.exists("Keywords")
    print(result)
