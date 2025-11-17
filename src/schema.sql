CREATE TABLE viitteet (
  id SERIAL PRIMARY KEY,

  /* Pääasialliset metatiedot*/
  type TEXT NOT NULL,
  year INTEGER NOT NULL,
  title TEXT NOT NULL,
  author TEXT[] NOT NULL,
  publisher TEXT,

  /* Erinäiset tunnisteet */
  doi TEXT,
  isbn TEXT,
  uri TEXT

  /*
  Mahdolliset kentät viitetyypeille

  book:
    year
    title
    author
    publisher
    doi
    isbn
    uri
  */
)