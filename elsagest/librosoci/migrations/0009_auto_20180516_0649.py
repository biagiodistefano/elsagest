# Generated by Django 2.0.2 on 2018-05-16 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librosoci', '0008_auto_20180516_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModificheSoci',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField()),
                ('cognome', models.TextField()),
                ('data_di_nascita', models.DateField()),
                ('codice_fiscale', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('data_iscrizione', models.DateField()),
                ('scadenza_iscrizione', models.DateField()),
                ('attivo', models.BooleanField(default=True)),
                ('data_creazione', models.DateTimeField()),
                ('dati_dal', models.DateTimeField()),
                ('dati_al', models.DateTimeField(auto_now_add=True)),
                ('ruolo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.Consigliere')),
                ('sezione', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.SezioneElsa')),
            ],
        ),
        migrations.CreateModel(
            name='RinnovoIscrizione',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_rinnovo', models.DateField()),
                ('quota_rinnovo', models.FloatField()),
            ],
            options={
                'db_table': 'rinnovi',
            },
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField()),
                ('cognome', models.TextField()),
                ('data_di_nascita', models.DateField()),
                ('codice_fiscale', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('data_iscrizione', models.DateField()),
                ('scadenza_iscrizione', models.DateField()),
                ('attivo', models.BooleanField(default=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('ruolo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.Consigliere')),
                ('sezione', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.SezioneElsa')),
            ],
            options={
                'db_table': 'soci',
            },
        ),
        migrations.AddField(
            model_name='rinnovoiscrizione',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.Socio'),
        ),
        migrations.AddField(
            model_name='modifichesoci',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.Socio'),
        ),
    ]
