import db_helper

def add_reference(index,title,type,year,author,organization,isbn,doi,url,publisher):
        authors = [a.strip() for a in author.split(",") if a.strip()]
        sql = """INSERT INTO viitteet (index, title, type, year, author, organization, isbn, doi, uri, publisher) VALUES (:index, :title, :type, :year, :author, :organization, :publisher, :isbn,:doi, :url) RETURNING id"""
        db_helper.execute(sql, {"index":index, "title": title, "type": type, "year": year, "author": authors, "organization":organization, "isbn":isbn, "doi":doi, "url":url, "publisher":publisher})

        return db_helper.last_insert_id()

def get_all_references():
    sql = "SELECT * FROM viitteet ORDER BY id"
    return db_helper.query(sql)