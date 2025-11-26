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
  doi TEXT,
  isbn TEXT,
  organization TEXT,
  uri TEXT

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

  Työn alla:
  
  inproceedings:
    booktitle
    organization
    publisher
  */
)