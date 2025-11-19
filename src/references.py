import db_helper

def add_reference(title,type,year,author):
        authors = [a.strip() for a in author.split(",") if a.strip()]
        sql = """INSERT INTO viitteet (title, type, year, author) VALUES (:title, :type, :year, :author) RETURNING id"""
        db_helper.execute(sql, {"title": title, "type": type, "year": year, "author": authors})

        return db_helper.last_insert_id()

def get_all_references():
    sql = "SELECT * FROM viitteet ORDER BY id"
    return db_helper.query(sql)