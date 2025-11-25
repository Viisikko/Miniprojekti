from db_helper import query

COLUMN_TO_BIBTEX = {
    "publisher": "publisher",
    "journal": "journal",
    "revision": "edition",   # bibtexissä kentän tunnisteena edition
    "doi": "doi",
    "isbn": "isbn",
    "uri": "url",
    "booktitle": "booktitle",
    "organization": "organization",
}


def escape_bibtex_value(value: str) -> str:
    if value is None:
        return ""
    s = str(value)
    # Jottei aaltosulkeet viitteen nimessä riko exporteria
    s = s.replace("{", "\\{").replace("}", "\\}")
    return s


def row_to_bibtex(row: dict) -> str:
    entry_type = (row["type"] or "misc").strip()
    key = row["index"]

    authors = row["author"] or []
    if isinstance(authors, list):
        author_str = " and ".join(authors)
    else:
        author_str = str(authors)

    fields = {
        "author": author_str,
        "title": row["title"],
        "year": str(row["year"]),
    }

    for col_name, bib_name in COLUMN_TO_BIBTEX.items():
        if col_name in row:
            value = row[col_name]
            if value not in (None, ""):
                fields[bib_name] = value

    lines = [f"@{entry_type}{{{key},"]

    items = list(fields.items())

    for field, value in items:
        val_str = escape_bibtex_value(value)
        lines.append(f"  {field} = {{{val_str}}},")

    lines.append("}")
    return "\n".join(lines)


def export_viitteet_to_bibtex(
    where_clause: str | None = None,
    params: dict | None = None,
) -> str:
    sql = "SELECT * FROM viitteet"

    # Tää johtaa SQL-injektioon jos where_clause on käyttäjän hallittavissa
    # Filtteröintiä varten jatkossa
    if where_clause:
        sql += " WHERE " + where_clause
    sql += " ORDER BY id"

    rows = query(sql, params or {})

    entries = [row_to_bibtex(row) for row in rows] # type: ignore
    content = "\n\n".join(entries) + ("\n" if entries else "")

    return content
