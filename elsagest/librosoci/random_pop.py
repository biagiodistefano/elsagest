from datetime import date, timedelta
import random
import sqlite3
import re
from .models import Socio, Ruolo, SezioneElsa, RuoliSoci
from django.contrib.auth.models import User
from tqdm import tqdm


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

sezioni_elsa = "Nessuna - Italia - Bari - Benevento - Bologna - Brescia - Cagliari - Campobasso - Castellanza - Catania - Cosenza  - Firenze - Genova - Lecce - Macerata - Messina - Milano - Modena & Reggio Emilia (MORE) - Napoli - Padova - Palermo - Parma - Pavia - Perugia - Pisa - Roma - Salerno - Sassari - Siena - Santa Maria Capua Vetere (SMCV) - Taranto - Teramo - Trento - Trieste - Udine - Urbino"

sezioni_elsa = [s.strip() for s in sezioni_elsa.split('-')]


ruoli = ["Presidente", "Segretario Generale", "Tesoriere", "VP Marketing",
         "VP Attività Accademiche", "VP Seminari e Conferenze", "VP STEP",
         "Director IM", "Director Tesoreria", "Director Marketing", "Director Attività Accademiche",
         "Director Seminari e Conferenze", "Director STEP"]

ruoli = [r + " Nazionale" for r in ruoli if r != "Socio"] + ruoli


def genera_ruoli():
    if not Ruolo.objects.all():
        for ruolo in ruoli:
            consigliere = Ruolo.objects.create(ruolo=ruolo)
            consigliere.save()


def genera_socio_random(numero_tessera, sezione):
    nome, cognome = random.choice(nomi).title(), random.choice(cognomi).title()
    data_iscrizione = random_date(date(2017, 1, 1), date.today() - timedelta(days=10))
    scadenza_iscrizione = data_iscrizione + timedelta(days=364)
    socio = dict(
        nome=nome,
        cognome=cognome,
        sezione=sezione,
        numero_tessera=numero_tessera,
        codice_fiscale="XXXXXX00XXXX11991",
        email=re.sub(r"[,']", r"", "".join(f"{nome}.{cognome}{random.randint(1, 100)}@example.com".lower().split())),
        data_iscrizione=data_iscrizione,
        scadenza_iscrizione=scadenza_iscrizione,
        attivo=True,
        quota_iscrizione=10
    )
    return socio


def genera_consigli_direttivi():
    for sezione in tqdm(list(SezioneElsa.objects.all()), desc="Genero consigli direttivi"):
        if sezione.nome == "Nessuna":
            continue
        if sezione.nome != "Italia":
            ruoli = list(Ruolo.objects.filter(id__gte=14))
            soci = list(Socio.objects.filter(sezione=sezione))
            while ruoli:
                ruolo = ruoli.pop()
                socio = soci.pop()
                ruolo_socio = RuoliSoci.objects.create(ruolo=ruolo, socio=socio, consigliere_dal=date.today())
                ruolo_socio.save()
        else:
            ruoli = list(Ruolo.objects.filter(id__lte=13))
            soci = list(Socio.objects.exclude(ruolo_socio__in=Ruolo.objects.filter(id__gte=14)))
            random.shuffle(soci)
            while ruoli:
                ruolo = ruoli.pop()
                socio = soci.pop()
                ruolo_socio = RuoliSoci.objects.create(ruolo=ruolo, socio=socio, consigliere_dal=date.today())
                ruolo_socio.save()


def genera_utenti():
    for sezione in SezioneElsa.objects.all():
        username = re.sub(r"[,']", r"", "".join(f"presidente.elsa{sezione.nome}".lower().split()))
        user = User.objects.create_user(username=username, password="elsa2018")
        user.set_password("elsa2018")
        user.save()
        user.userprofile.sezione = sezione
        user.save()
    superuser = User.objects.create_superuser(username="biagio",
                                    first_name="Biagio",
                                    last_name="Distefano",
                                    email="biagiodistefano92@gmailcom",
                                    is_staff=True,
                                    is_superuser=True, password="elsa2018")  # cambiata al primo login
    # superuser.set_password("ElsaMaster2018")
    superuser.save()


def genera_sezioni():
    if not SezioneElsa.objects.all():
        genera_ruoli()
        for nome_sezione in tqdm(sezioni_elsa, desc="Genero sezioni"):
            sezione = SezioneElsa.objects.create(nome=nome_sezione)
            sezione.save()
            if nome_sezione in ["Nessuna", "Italia"]:
                continue
            Socio.objects.bulk_create([Socio(**genera_socio_random(x, sezione)) for x in tqdm(list(range(random.randint(50, 200))), desc="Genreo soci")])

        genera_consigli_direttivi()
        genera_utenti()
    else:
        print("Niente da generare")


# genera_sezioni()


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
