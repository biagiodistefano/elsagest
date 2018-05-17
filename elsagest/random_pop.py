from datetime import date, timedelta
import random
import sqlite3
import argparse
import re

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--dry', action="store_true", help="Do not update db")


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
cur = conn.cursor()

sezioni = "Nessuna - Italia - Bari - Benevento - Bologna - Brescia - Cagliari - Campobasso - Castellanza - Catania - Cosenza  - Firenze - Genova - Lecce - Macerata - Messina - Milano - Modena & Reggio Emilia (MORE) - Napoli - Padova - Palermo - Parma - Pavia - Perugia - Pisa - Roma - Salerno - Sassari - Siena - Santa Maria Capua Vetere (SMCV) - Taranto - Teramo - Trento - Trieste - Udine - Urbino"

sezioni = [s.strip() for s in sezioni.split('-')]


ruoli = ["Socio", "Presidente", "Segretario Generale", "Tesoriere", "VP Marketing",
         "VP Attività Accademiche", "VP Seminari e Conferenze", "VP STEP",
         "Director IM", "Director Tesoreria", "Director Marketing", "Director Attività Accademiche",
         "Director Seminari e Conferenze", "Director STEP"]

ruoli += [r + " Nazionale" for r in ruoli if r != "Socio"]


def genera_ruoli():
    with conn:
        for i, ruolo in enumerate(ruoli):
            cur.execute("""INSERT INTO ruoli_consiglieri (id, ruolo) VALUES (?, ?)""", (i, ruolo, ))


def genera_socio_random(numero_tessera, sezione_id):
    socio = dict(
        nome=random.choice(nomi).title(),
        cognome=random.choice(cognomi).title(),
        data_di_nascita=random_date(date(1990, 1, 1), date(2000, 5, 1)),
        data_iscrizione=random_date(date(2017, 1, 1), date.today()),
        numero_tessera=numero_tessera,
        codice_fiscale="XXXXXX00XXXX11991",
        ruolo_id=0,
        attivo=1,
        sezione_id=sezione_id,
        quota_iscrizione=10
    )
    socio['email'] = "".join(f"{socio['nome']}.{socio['cognome']}{random.randint(1, 100)}@example.com".lower().split())
    socio['email'] = re.sub(r"[,']", r"", socio["email"])
    scadenza_iscrizione = socio["data_iscrizione"] + timedelta(days=364)
    if scadenza_iscrizione < date.today():
        if random.choice([True, False]):
            socio['ultimo_rinnovo'] = random_date(scadenza_iscrizione, date.today())
            scadenza_iscrizione = socio['ultimo_rinnovo'] + timedelta(days=364)
        else:
            socio['ultimo_rinnovo'] = socio['data_iscrizione']
    else:
        socio['ultimo_rinnovo'] = socio['data_iscrizione']
    socio["scadenza_iscrizione"] = scadenza_iscrizione

    return socio


def genera_consigli_direttivi():
    consigli_direttivi = []
    for nome_sezione in sezioni:
        if nome_sezione in ["Nessuna"]:
            continue
        ruoli = ["presidente", "secgen", "tesoreria", "vpmarketing", "vpaa", "vpsc", "vpstep", "dirim", "dirtes", "dirmkt", "diraa", "dirsc", "dirstep"]
        ruoli = list(zip(ruoli, range(1, 14)))
        random.shuffle(ruoli)
        sezione_id = cur.execute("SELECT id FROM sezioni_elsa WHERE nome=?", (nome_sezione,)).fetchone()[0]
        if nome_sezione != "Italia":
            id_soci_sezione = [row[0] for row in cur.execute("SELECT id FROM soci WHERE sezione_id=?", (sezione_id,))]
        else:
            id_soci_sezione = [row[0] for row in cur.execute("SELECT id FROM soci") if row[0] not in consigli_direttivi]
        with conn:
            while ruoli:
                socio_id = random.choice(id_soci_sezione)
                id_soci_sezione.remove(socio_id)
                consigli_direttivi.append(socio_id)
                short, ruolo_id = ruoli.pop()
                if nome_sezione == "Italia":
                    ruolo_id += 13
                cur.execute(
                    """
                    UPDATE soci
                    SET ruolo_id=?, consigliere_dal=?
                    WHERE id=?
                    """, (ruolo_id, date.today() - timedelta(days=160), socio_id)
                )
                email = "".join(f"{short}@elsa-{nome_sezione}.org".split()).lower()
                cur.execute(
                    """
                    INSERT OR IGNORE INTO email_consiglieri (email, ruolo_id, socio_id) VALUES (?, ?, ?)
                    """, (email, ruolo_id, socio_id)
                )


def genera_sezioni():
    for nome_sezione in sezioni:
        with conn:
            cur.execute(
                """
                INSERT INTO sezioni_elsa (nome) VALUES (?)
                """, (nome_sezione, )
            )
            if nome_sezione in ["Nessuna", "Italia"]:
                continue

            sezione_id = cur.lastrowid
            for x in range(random.randint(50, 200)):
                socio = genera_socio_random(x, sezione_id=sezione_id)
                cur.execute(
                    """
                    INSERT INTO soci (
                      nome, cognome, email, data_iscrizione, codice_fiscale, sezione_id,
                      scadenza_iscrizione, attivo, data_creazione, ruolo_id, numero_tessera, ultimo_rinnovo, quota_iscrizione
                    ) VALUES (:nome, :cognome, :email, :data_iscrizione, :codice_fiscale,
                    :sezione_id, :scadenza_iscrizione, :attivo, CURRENT_TIMESTAMP, :ruolo_id, :numero_tessera, :ultimo_rinnovo, :quota_iscrizione)
                    """, socio
                )

genera_ruoli()
genera_sezioni()
genera_consigli_direttivi()


"""
insert into email_consiglieri (email, ruolo_id, socio_id) values ('presidente@elsasiena.org', 1, 5);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('secgen@elsasiena.org', 2, 6);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('tesoriere@elsasiena.org', 3, 7);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('vpmarketing@elsasiena.org', 4, 8);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('vpaa@elsasiena.org', 5, 9);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('vpsc@elsasiena.org', 6, 10);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('vpstep@elsasiena.org', 7, 11);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('dirim@elsasiena.org', 8, 12);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('dirtesoreria@elsasiena.org', 9, 13);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('dirmarketing@elsasiena.org', 10, 14);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('dirsc@elsasiena.org', 11, 15);
insert into email_consiglieri (email, ruolo_id, socio_id) values ('dirstep@elsasiena.org', 12, 16);
"""
