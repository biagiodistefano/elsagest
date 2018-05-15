from datetime import date, timedelta
import random
import sqlite3


def random_date(d1, d2):
    delta = d2 - d1
    random_delta = random.randint(1, delta.days)
    new_date = d1 + timedelta(days=random_delta)
    return new_date


with open('nomi.txt', 'r') as f:
    nomi = [n.strip() for n in f.readlines()]

with open('cognomi.txt', 'r') as f:
    cognomi = [c.strip() for c in f.readlines()]


conn = sqlite3.connect("db.sqlite3")

with conn:
    cur = conn.cursor()
    for x in range(100):
        nome = random.choice(nomi).title()
        cognome = random.choice(cognomi).title()
        email = "".join(f"{nome}.{cognome}{random.randint(1, 100)}@example.com".lower().split())
        data_di_nascita = random_date(date(1990, 1, 1), date(2000, 5, 1))
        data_iscrizione = random_date(date(2017, 1, 1), date.today())
        scadenza_iscrizione = data_iscrizione + timedelta(days=365)
        codice_fiscale = "XXXXXX00XXXX11991"
        sezione_id = 1
        cur.execute(
            """
            INSERT INTO soci (
              nome, cognome, email, data_di_nascita, data_iscrizione, codice_fiscale, sezione_id, scadenza_iscrizione, attivo
            ) VALUES (? ,? ,?, ?, ?, ?, ?, ?, ?)
            """, (nome, cognome, email, data_di_nascita, data_iscrizione, codice_fiscale, sezione_id, scadenza_iscrizione, True)
        )
