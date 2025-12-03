# Miniprojekti

## Linkkejä
Linkki backlogiin
https://github.com/orgs/Viisikko/projects/1
<br>
Linkki demoon
https://limousines-bless-bag-memory.trycloudflare.com/login

## Definition of done:
- sovellus käynnistyy ilman virheitä
- koodi on peer reviewattu
- github actionsin CI toimii ilman virheitä
- storyn hyväksymiskriteerit täyttyy

## Konfigurointi

`.env` tiedoston kasaaminen
```
DATABASE_URL=postgresql://postgres@localhost/ohtu
SECRET_KEY=<satunnaista>
USERCONFIG="outi:12345"
```

Tuotantopalvelimen konfiguraatio: `src/gunicorn.conf.py`


## Tuotantopalvelimella ajaminen

Ympäristön alustus ja riippuvuuksien asennus:
```
git clone https://github.com/Viisikko/Miniprojekti.git
cd Miniprojekti
uv venv
uv add -r requirements.txt
```

Minimaalinen konfigurointi ja tietokannan alustus:
```
# luo .env tiedosto ylläolevien ohjeiden mukaan
python src/db_helper.py
```

Sovelluspalvelimen käynnistys (suorita `src`-hakemistossa):
```bash
gunicorn -c gunicorn.conf.py index:app
```

Oletuskonfiguraatiolla sovelluspalvelin kuuntelee vain loopback-osoitetta (127.0.0.1) portissa 5001. Konfiguraatiota voi muokata `src/gunicorn.conf.py`-tiedostossa. Oletuskonfiguraatio on tehty olettaen että sovelluksen edessä olisi reverse-proxy (tuotannossa tällä hetkellä käytössä `cloudflared`, mutta ei pitäisi vaatia erikoisempaa konfiguraatiota vaihtaa toiseen). 