from flask import redirect, render_template, request, jsonify, flash, url_for, g, session, send_file, Response
from config import app, test_env, user, db
from functools import wraps
import references
import generate_bibtex
from sqlalchemy import text
import requests


def require_login():
    def login_wrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):
            if session:
                if session["user"] != None:
                    return f(*args, **kwargs)
            return redirect(url_for('login'), 302)
        return decorated_f
    return login_wrapper


@app.route("/")
@require_login()
def index():
    search_query = ""
    if request.args.get("q"):
        search_query = request.args.get("q")
        references_list = references.search_references(search_query)
    else:
        references_list = references.get_all_references()

    return render_template("index.html", references=references_list, search_query=search_query)


@app.route("/", methods=["POST"])
def login_post():
    if ("username" in request.form) and ("password" in request.form):
        if (request.form["username"] == user[0]) and (request.form["password"] == user[1]):
            session["user"] = user[0]
            return redirect(url_for("index"), 302)
    return "Väärä käyttäjätunnus tai salasana", 403


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/add_reference")
@require_login()
def add_reference():
    return render_template("add_reference.html")


@app.route("/create_reference", methods=["POST"])
@require_login()
def create_reference():
    def get_param(x):
        return request.form.get(x, "").strip()

    title = get_param("title")
    reference_type = get_param("type")
    year_raw = get_param("year")
    author = get_param("author")
    index = get_param("index")
    isbn = get_param("isbn")
    doi = get_param("doi")
    journal = get_param("journal")
    url = get_param("url")
    organization = get_param("organization")
    booktitle = get_param("booktitle")
    publisher = get_param("publisher")
    category = get_param("category")

    if not title or len(title) > 512:
        return "Error: Title must be between 1 and 512 characters.<br> <a href='/add_reference'>Return to reference creation</a>", 400

    if not year_raw:
        return "Error: Year is required.<br> <a href='/add_reference'>Return to reference creation</a>", 400

    try:
        year = int(year_raw)
    except ValueError:
        return "Error: Year must be a number.<br> <a href='/add_reference'>Return to reference creation</a>", 400

    if year < 868 or year > 2099:
        return "Error: Year cannot be under 868 or too much in the future.<br> <a href='/add_reference'>Return to reference creation</a>", 400

    if not author or len(author) < 3:
        return "Error: Author must be at least 3 characters long.<br> <a href='/add_reference'>Return to reference creation</a>", 400
    if not index:
        return "Error: Index is required", 400

    if references.get_reference_by_index(index) != None:
        return "Error: Index must be unique", 400

    reference_id = None

    def to_strval(x): return x if x != None else ""
    search_str = ' '.join(
        f"{title} {author.replace(",", " ")} {year} {to_strval(journal)} {to_strval(publisher)} {to_strval(booktitle)}".strip().split())

    match reference_type:
        case "book":
            # reference_id = references.add_reference(
            #    index, title, reference_type, year, author, organization, isbn, doi, url, publisher, category)

            # Korvattu toistaiseksi samalla toteutuksella kun muut
            result = db.session.execute(text("INSERT INTO viitteet (index, title, type, year, author, organization, doi, isbn, publisher, uri, search_str, category) VALUES (:index, :title, :type, :year, :author, :organization, :doi, :isbn, :publisher, :uri, :search_str, :category) RETURNING id"),
                                        {"index": index, "title": title, "type": reference_type, "year": year, "author": list(map(lambda x: x.strip(), author.split(","))), "organization": organization, "doi": doi, "isbn": isbn, "publisher": publisher, "uri": url, "search_str": search_str, "category": list(map(lambda x: x.strip(), category.split(",")))})
            db.session.commit()
            reference_id = result.fetchone()

        case "article":
            result = db.session.execute(text("INSERT INTO viitteet (index, title, type, year, author, doi, journal, category, search_str, uri) VALUES (:index, :title, :type, :year, :author, :doi, :journal, :category, :search_str, :uri) RETURNING id"),
                                        {"index": index, "title": title, "type": reference_type, "year": year, "author": list(map(lambda x: x.strip(), author.split(","))), "category": list(map(lambda x: x.strip(), category.split(","))),  "doi": doi, "journal": journal, "search_str": search_str, "uri":url})
            db.session.commit()
            reference_id = result.fetchone()
        case "misc":
            result = db.session.execute(text("INSERT INTO viitteet (index, title, type, year, author, uri,category, search_str) VALUES (:index, :title, :type, :year, :author, :url, :category, :search_str) RETURNING id"),
                                        {"index": index, "title": title, "type": reference_type, "url": url, "year": year, "category": list(map(lambda x: x.strip(), category.split(","))), "author": list(map(lambda x: x.strip(), author.split(","))), "search_str": search_str})
            db.session.commit()
            reference_id = result.fetchone()
        case "inproceedings":
            if not booktitle:
                return "Error: lisää booktitle"

            result = db.session.execute(text("INSERT INTO viitteet (index, title, type, year, author, booktitle, organization, uri, publisher, category, search_str) VALUES (:index, :title, :type, :year, :author, :booktitle, :organization, :url, :publisher, :category, :search_str) RETURNING id"),
                                        {"index": index, "title": title, "type": reference_type, "year": year, "category": list(map(lambda x: x.strip(), category.split(","))), "author": list(map(lambda x: x.strip(), author.split(","))), "url": url, "booktitle": booktitle, "organization": organization, "publisher": publisher, "search_str": search_str})
            db.session.commit()
            reference_id = result.fetchone()
        case _:
            return "Epäkelpo viitetyyppi", 400

    if not reference_id:
        return "Error: Could not create reference", 500
    return redirect("/")


@app.route("/index/<index>")
@require_login()
def check_index(index):
    if index:
        return {"status": references.get_reference_by_index(index) != None}
    return "not a valid index", 400


@app.route("/metadata")
@require_login()
def get_metadata():
    doi = request.args.get("doi")
    if doi:
        api_response = requests.get(
            f"https://api.crossref.org/works/doi/{doi}")

        if api_response.status_code != 200:
            return "external api error", 500
        try:
            api_json = api_response.json()["message"]
        except requests.exceptions.JSONDecodeError:
            return "external api responded with invalid data", 500

        return {
            "author": list(map(lambda x: f"{x["given"]} {x["family"]}", api_json["author"])),
            "publisher": api_json["publisher"],
            "title": api_json["title"][0] if len(api_json["title"]) > 0 else None,
            "year": api_json["published"]["date-parts"][0][0] if ("date-parts" in api_json["published"]) and (len(api_json["published"]["date-parts"]) > 0) else None,
            "journal": api_json["container-title"][0] if ("container-title" in api_json) and (len(api_json["container-title"]) > 0) else None,
            "url": api_json["link"][0]["URL"] if len(api_json["link"]) > 0 else None
        }
    
    return "invalid request", 400


@app.route('/export_bibtex')
def export_bibtex():
    bibtex_string = generate_bibtex.export_viitteet_to_bibtex()
    return Response(
        bibtex_string,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=references.bib"}
    )


@app.route("/delete_reference", methods=["POST"])
@require_login()
def delete_reference():
    ref_id = request.form["id"]
    references.delete_reference(ref_id)
    return redirect("/")


@app.route("/edit_reference/<int:ref_id>", methods=["GET"])
@require_login()
def edit_reference(ref_id):
    ref = references.get_reference_by_id(ref_id)
    if not ref:
        return redirect("/")

    ref_data = dict(ref)
    if ref_data["author"]:
        ref_data["author"] = ", ".join(ref_data["author"])

    if ref_data["category"]:
        ref_data["category"] = ", ".join(ref_data["category"])
    else:
        ref_data["category"] = ""


    return render_template("add_reference.html", ref=ref_data)


@app.route("/update_reference", methods=["POST"])
@require_login()
def update_reference():
    def get_param(x):
        return request.form.get(x, "").strip()

    # Otetaan ID talteen, jotta tiedetään mitä riviä päivitetään
    ref_id = get_param("id")

    title = get_param("title")
    year_raw = get_param("year")
    author = get_param("author")
    index = get_param("index")
    isbn = get_param("isbn")
    doi = get_param("doi")
    journal = get_param("journal")
    url = get_param("url")
    organization = get_param("organization")
    booktitle = get_param("booktitle")
    publisher = get_param("publisher")
    category = get_param("category")

    # --- SAMA VALIDOINTI KUIN CREATE_REFERENCE ---
    if not title or len(title) > 512:
        return "Error: Title must be between 1 and 512 characters.", 400

    if not year_raw:
        return "Error: Year is required.", 400

    try:
        year = int(year_raw)
    except ValueError:
        return "Error: Year must be a number.", 400

    if year < 868 or year > 2099:
        return "Error: Year cannot be under 868 or too much in the future.", 400

    if not author or len(author) < 3:
        return "Error: Author must be at least 3 characters long.", 400
    if not index:
        return "Error: Index is required", 400

    # Haetaan kannasta viitteen tiedot, sekä mahdolliset pyydetyn indeksin omaava viite
    references_by_index = references.get_reference_by_index(index)
    references_by_id = references.get_reference_by_id(ref_id)

    if references_by_id == None:
        return "Error: Not a valid reference id", 400

    # Napataan tyyppi kannasta, käyttäjän ei pitäisi tätä pystyä muuttamaan luomisen jälkeen
    reference_type = references_by_id["type"]

    # Tarkistetaan ettei indeksiä ole jo kannassa, paitsi jos se on muutettavan viitteen oma
    if references_by_index != None:
        if references_by_id["id"] != references_by_index["id"]:
            return "Error: Index must be unique", 400

    # Muutetaan author-string listaksi tietokantaa varten (kuten create-funktiossa)
    author_list = list(map(lambda x: x.strip(), author.split(",")))
    category_list = list(map(lambda x: x.strip(), category.split(",")))

    def to_strval(x): return x if x != None else ""
    search_str = ' '.join(
        f"{title} {author.replace(",", " ")} {year} {to_strval(journal)} {to_strval(publisher)} {to_strval(booktitle)}".strip().split())

    match reference_type:
        case "book":
            # Jos sinulla on references.py:ssä update_reference, käytä sitä.
            # Tässä kuitenkin sama raaka-SQL tyyli varmuuden vuoksi, jotta "index"-virhe ei toistu:
            sql = text('UPDATE viitteet SET "index"=:index, title=:title, year=:year, author=:author, category=:category, organization=:organization, isbn=:isbn, doi=:doi, uri=:url, publisher=:publisher, search_str=:search_str WHERE id=:id')
            db.session.execute(sql, {"id": ref_id, "index": index, "title": title, "year": year, "author": author_list, "category": category_list,
                               "organization": organization, "isbn": isbn, "doi": doi, "url": url, "publisher": publisher, "search_str": search_str})
            db.session.commit()

        case "article":
            # HUOM: "index" lainausmerkeissä
            sql = text(
                'UPDATE viitteet SET "index"=:index, title=:title, year=:year, author=:author,category=:category, doi=:doi, journal=:journal, search_str=:search_str, uri=:url WHERE id=:id')
            db.session.execute(sql, {"id": ref_id, "index": index, "title": title,
                               "year": year, "author": author_list, "category": category_list, "doi": doi, "journal": journal, "search_str": search_str, "url":url})
            db.session.commit()

        case "misc":
            # HUOM: "index" lainausmerkeissä
            sql = text(
                'UPDATE viitteet SET "index"=:index, title=:title, year=:year, author=:author,category=:category, uri=:url, search_str=:search_str WHERE id=:id')
            db.session.execute(sql, {"id": ref_id, "index": index, "title": title,
                               "year": year, "author": author_list, "category": category_list, "url": url, "search_str": search_str})
            db.session.commit()

        case "inproceedings":
            if not booktitle:
                return "Error: lisää booktitle"

            # HUOM: "index" lainausmerkeissä
            sql = text('UPDATE viitteet SET "index"=:index, title=:title, year=:year, author=:author,category=:category, booktitle=:booktitle, organization=:organization, uri=:url, publisher=:publisher, search_str=:search_str WHERE id=:id')
            db.session.execute(sql, {"id": ref_id, "index": index, "title": title, "year": year, "author": author_list, "category": category_list,
                               "booktitle": booktitle, "organization": organization, "url": url, "publisher": publisher, "search_str": search_str})
            db.session.commit()

        case _:
            return "Epäkelpo viitetyyppi", 400

    return redirect("/")
