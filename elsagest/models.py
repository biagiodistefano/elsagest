# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EmailConsiglieri(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    email = models.CharField(max_length=254)
    ruolo = models.ForeignKey('RuoliConsiglieri', models.DO_NOTHING)
    socio = models.ForeignKey('Soci', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_consiglieri'


class LibrosociHistoricalemailconsigliere(models.Model):
    id = models.IntegerField()
    email = models.CharField(max_length=254)
    history_id = models.IntegerField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    ruolo_id = models.IntegerField(blank=True, null=True)
    socio_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'librosoci_historicalemailconsigliere'


class LibrosociHistoricalrinnovoiscrizione(models.Model):
    id = models.IntegerField()
    data_rinnovo = models.DateField()
    quota_rinnovo = models.FloatField()
    history_id = models.IntegerField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    socio_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'librosoci_historicalrinnovoiscrizione'


class LibrosociHistoricalsocio(models.Model):
    id = models.IntegerField()
    nome = models.TextField()
    cognome = models.TextField()
    numero_tessera = models.IntegerField()
    codice_fiscale = models.TextField()
    email = models.CharField(max_length=254)
    data_iscrizione = models.DateField()
    quota_iscrizione = models.FloatField()
    scadenza_iscrizione = models.DateField()
    ultimo_rinnovo = models.DateField()
    attivo = models.BooleanField()
    consigliere_dal = models.DateField(blank=True, null=True)
    data_creazione = models.DateTimeField()
    history_id = models.IntegerField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    ruolo_id = models.IntegerField(blank=True, null=True)
    sezione_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'librosoci_historicalsocio'


class LibrosociHistoricaluserprofile(models.Model):
    id = models.IntegerField()
    history_id = models.IntegerField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    sezione_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'librosoci_historicaluserprofile'


class LibrosociUserprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    sezione = models.ForeignKey('SezioniElsa', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'librosoci_userprofile'


class Rinnovi(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    data_rinnovo = models.DateField()
    quota_rinnovo = models.FloatField()
    socio = models.ForeignKey('Soci', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rinnovi'


class RuoliConsiglieri(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    ruolo = models.TextField()

    class Meta:
        managed = False
        db_table = 'ruoli_consiglieri'


class SezioniElsa(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    nome = models.TextField()

    class Meta:
        managed = False
        db_table = 'sezioni_elsa'


class SezioniElsaUsers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    sezioneelsa = models.ForeignKey(SezioniElsa, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sezioni_elsa_users'
        unique_together = (('sezioneelsa', 'user'),)


class Soci(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    nome = models.TextField()
    cognome = models.TextField()
    codice_fiscale = models.TextField()
    email = models.CharField(max_length=254)
    data_iscrizione = models.DateField()
    scadenza_iscrizione = models.DateField()
    attivo = models.BooleanField()
    data_creazione = models.DateTimeField()
    ruolo = models.ForeignKey(RuoliConsiglieri, models.DO_NOTHING, blank=True, null=True)
    sezione = models.ForeignKey(SezioniElsa, models.DO_NOTHING)
    numero_tessera = models.IntegerField()
    ultimo_rinnovo = models.DateField()
    consigliere_dal = models.DateField(blank=True, null=True)
    quota_iscrizione = models.FloatField()

    class Meta:
        managed = False
        db_table = 'soci'
