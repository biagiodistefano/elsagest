# Generated by Django 2.0.2 on 2018-05-16 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librosoci', '0011_socio_ultimo_rinnovo'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='consigliere_dal',
            field=models.DateField(null=True),
        ),
    ]
