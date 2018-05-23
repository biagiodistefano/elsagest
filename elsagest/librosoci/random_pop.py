from datetime import date, timedelta
import random
import sqlite3
import re
from .models import Socio, Ruolo, SezioneElsa, Consigliere
from elsamail.models import UnsubscribeToken, Email, BozzaEmail
from django.contrib.auth.models import User
from tqdm import tqdm
import uuid
import lorem
from bs4 import BeautifulSoup


def random_date(d1, d2):
    delta = d2 - d1
    random_delta = random.randint(1, delta.days)
    new_date = d1 + timedelta(days=random_delta)
    return new_date


with open('nomi.txt', 'r') as f:
    nomi = [n.strip() for n in f.readlines()]

with open('cognomi.txt', 'r') as f:
    cognomi = [c.strip() for c in f.readlines()]


soup = BeautifulSoup(open("universitalia.html", "r"), "html.parser")
lista_universita = []
for a in soup.find_all("a"):
    href = a.get("href")
    if href and href.startswith("1"):
        codice = href.split(".")[0].replace("1", "").upper()
        uni = a.text.strip()
        lista_universita.append((uni, codice))


conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

sezioni_elsa = "Nessuna - Italia - Bari - Benevento - Bologna - Brescia - Cagliari - Campobasso - Castellanza - Catania - Cosenza  - Firenze - Genova - Lecce - Macerata - Messina - Milano - Modena & Reggio Emilia (MORE) - Napoli - Padova - Palermo - Parma - Pavia - Perugia - Pisa - Roma - Salerno - Sassari - Siena - Santa Maria Capua Vetere (SMCV) - Taranto - Teramo - Trento - Trieste - Udine - Urbino"

sezioni_elsa = [s.strip() for s in sezioni_elsa.split('-')]


ruoli = [("Presidente", "presidente"), ("Segretario Generale", "secgen"), ("Tesoriere", "tesoriere"),
         ("VP Marketing", "vpmkt"), ("VP Attività Accademiche", "vpaa"), ("VP Seminari e Conferenze", "vpsc"),
         ("VP STEP", "vpstep"),
         ("Director IM", "dirim"), ("Director Tesoreria", "dirtes"), ("Director Marketing", "dirmkt"),
         ("Director Attività Accademiche", "diraa"), ("Director Seminari e Conferenze", "dirsc"),
         ("Director STEP", "dirstep")]

ruoli = [(r + " Nazionale", s) for r, s in ruoli] + ruoli


def genera_ruoli():
    if not Ruolo.objects.all():
        for ruolo, abbreviazione in ruoli:
            ruolo = Ruolo.objects.create(ruolo=ruolo, abbreviazione=abbreviazione)
            ruolo.save()


def cellulare_random():
    prefisso = f"3{random.randint(0, 88)}"
    numero = f"{prefisso} {random.randint(10000000, 99999999)}" # li generiamo di 8 cifre anziché di 7 così sicuro non esistono
    return numero


def universita_random(sezione):
    choices = [codice for uni, codice in lista_universita if sezione.nome.lower() in uni.lower()]
    if choices:
        return random.choice(choices)
    else:
        return random.choice([codice for uni, codice in lista_universita])


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
        cellulare=cellulare_random(),
        universita=universita_random(sezione),
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
                email = f"{ruolo.abbreviazione}@{sezione.domain}.org"
                consigliere = Consigliere.objects.create(
                    ruolo=ruolo,
                    socio=socio,
                    sezione=sezione,
                    consigliere_dal=date.today(),
                    email=email
                )
                consigliere.save()
        else:
            ruoli = list(Ruolo.objects.filter(id__lte=13))
            soci = list(Socio.objects.exclude(ruolo_socio__in=Ruolo.objects.filter(id__gte=14)))
            random.shuffle(soci)
            while ruoli:
                ruolo = ruoli.pop()
                socio = soci.pop()
                email = f"{ruolo.abbreviazione}@{sezione.domain}.org"
                consigliere = Consigliere.objects.create(
                    ruolo=ruolo,
                    socio=socio,
                    sezione=sezione,
                    consigliere_dal=date.today(),
                    email=email
                )
                consigliere.save()


def genera_utenti():
    for sezione in tqdm(list(SezioneElsa.objects.all()), desc="Genero utenti"):
        username = re.sub(r"[,']", r"", "".join(f"presidente.elsa{sezione.denominazione}".lower().split()))
        user = User.objects.create_user(username=username, password="elsa2018")
        # user.set_password("elsa2018")
        # user.save()
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


def genera_unsubscribe_token():
    for socio in tqdm(list(Socio.objects.all()), desc="Genero token"):
        token = uuid.uuid4()
        ut = UnsubscribeToken.objects.create(socio=socio, token=token)


def genera_finte_email():
    for user in tqdm(list(User.objects.all()), desc="Genero email"):
        for x in range(5):
            email = Email(
                oggetto=lorem.sentence(),
                corpo=f"<h4>{lorem.sentence()}</h4><p>{lorem.paragraph()}</p>",
                mittente=user
            )
            email.save()
        for x in range(5, random.randint(10, 15)):
            if user.userprofile.sezione.nome == 'Italia':
                disponibile_per = random.choice([0, 1, 2])
            else:
                disponibile_per = random.choice([0, 1])
            bozza = BozzaEmail(
                oggetto=lorem.sentence(),
                corpo=f"<h4>{lorem.sentence()}</h4><p>{lorem.paragraph()}</p>",
                user=user,
                disponibile_per=disponibile_per
            )
            bozza.save()


def genera_sezioni():
    if not SezioneElsa.objects.all():
        genera_ruoli()
        for nome_sezione in tqdm(sezioni_elsa, desc="Genero sezioni"):
            sezione = SezioneElsa.objects.create(nome=nome_sezione)
            sezione.save()
            if nome_sezione in ["Nessuna", "Italia"]:
                continue
            Socio.objects.bulk_create([Socio(**genera_socio_random(x, sezione)) for x in tqdm(list(range(random.randint(50, 200))), desc="Genreo soci")])

        genera_unsubscribe_token()
        genera_consigli_direttivi()
        genera_utenti()
        genera_finte_email()
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
