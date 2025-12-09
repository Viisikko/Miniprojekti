CREATE TABLE viitteet (
  id SERIAL PRIMARY KEY,

  /* Pääasialliset metatiedot*/
  type TEXT NOT NULL,
  index TEXT UNIQUE NOT NULL,
  year INTEGER NOT NULL,
  title TEXT NOT NULL,
  author TEXT[] NOT NULL,
  publisher TEXT,
  revision TEXT,
  journal TEXT,
  booktitle TEXT, 

  /* Erinäiset tunnisteet */
  doi TEXT UNIQUE,
  isbn TEXT,
  organization TEXT,
  uri TEXT,

  /* Kategoria */
  category TEXT[],

  /* Haku */
  search_str TEXT NOT NULL,
  hakuvektori TSVECTOR
      GENERATED ALWAYS AS (to_tsvector('simple', search_str)) STORED

  /*
  Mahdolliset kentät viitetyypeille

  common:
    year
    title
    author
    uri

  book:
    publisher
    doi
    isbn
  
  article:
    journal
    doi
  
  inproceedings:
    booktitle
    organization
    publisher
  */
);

CREATE INDEX viitteet_haku ON viitteet USING gin(hakuvektori);