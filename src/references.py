import db_helper

def add_reference(index,title,type,year,author,organization,isbn,doi,url,publisher,category):
    authors = [a.strip() for a in author.split(",") if a.strip()]
    category = [b.strip() for b in category.split(",") if b.strip()]
    sql = """INSERT INTO viitteet (index, title, type, year, author, organization, isbn, doi, uri, publisher,category) VALUES (:index, :title, :type, :year, :author, :organization, :publisher, :isbn,:doi, :url, :category) RETURNING id"""
    db_helper.execute(sql, {"index":index, "title": title, "type": type, "year": year, "author": authors, "organization":organization, "isbn":isbn, "doi":doi, "url":url, "publisher":publisher, "category":category})

    return db_helper.last_insert_id()

def get_all_references(sort_by="id", order="asc"):
    valid_sort_columns = ["id", "title", "type", "year", "author"]
    
    if sort_by not in valid_sort_columns:
        sort_by = "id"

    if order.lower() != "desc":
        order = "asc"

    sql = f"SELECT * FROM viitteet ORDER BY {sort_by} {order}"
    
    return db_helper.query(sql)

def delete_reference(ref_id):
    sql = "DELETE FROM viitteet WHERE id = :id"
    db_helper.execute(sql, {"id": ref_id})

def get_reference_by_id(ref_id):
    sql = "SELECT * FROM viitteet WHERE id = :id"
    result = db_helper.query(sql, {"id": ref_id})
    return result[0] if result else None

def get_reference_by_index(ref_index):
    sql = "SELECT * FROM viitteet WHERE index = :index"
    result = db_helper.query(sql, {"index": ref_index})
    return result[0] if result else None

def search_references(search_terms):
    sql = "SELECT * FROM viitteet WHERE hakuvektori @@ websearch_to_tsquery('simple', :search_terms)"
    return db_helper.query(sql, {"search_terms": search_terms})


def update_reference(ref_id, index, title, type, year, author, organization, isbn, doi, url, publisher, journal, booktitle):
    authors = [a.strip() for a in author.split(",") if a.strip()]

    sql = """
        UPDATE viitteet 
        SET index=:index, title=:title, type=:type, year=:year, author=:author, 
            organization=:organization, isbn=:isbn, doi=:doi, uri=:uri, 
            publisher=:publisher, journal=:journal, booktitle=:booktitle
        WHERE id=:id
    """

    db_helper.execute(sql, {
        "id": ref_id,
        "index": index, 
        "title": title, 
        "type": type, 
        "year": year, 
        "author": authors, 
        "organization": organization, 
        "isbn": isbn, 
        "doi": doi, 
        "url": url, 
        "publisher": publisher,
        "journal": journal,
        "booktitle": booktitle
    })