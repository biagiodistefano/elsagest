# Generated by Django 2.0.2 on 2018-05-17 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librosoci', '0022_modifichesoci_quota_iscrizione'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='quota_iscrizione',
            field=models.FloatField(default=10.0),
            preserve_default=False,
        ),
    ]
