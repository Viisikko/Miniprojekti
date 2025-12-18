# Miniprojekti
[![CI](https://github.com/Viisikko/Miniprojekti/actions/workflows/main.yml/badge.svg)](https://github.com/Viisikko/Miniprojekti/actions/workflows/main.yml)
[![License](https://img.shields.io/github/license/Viisikko/Miniprojekti)](https://github.com/Viisikko/Miniprojekti/blob/main/LICENSE)
## Linkkejä
Linkki backlogiin
https://github.com/orgs/Viisikko/projects/1
<br>
Linkki demoon
https://limousines-bless-bag-memory.trycloudflare.com/login
<br>
linkki coverage reporttiin
https://github.com/Viisikko/Miniprojekti/blob/main/coverage/coverage.png
<br>
Tunnukset demoon: `outi:13740f660f57f97b`
<br>
Demo repo jossa kaikki sprint4 commitit jne. https://github.com/Viisikko/miniprojekti_demo
<br>
Ryhmän raportti https://github.com/Viisikko/Miniprojekti/blob/main/Viisikko_miniprojekti_raportti.pdf

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
