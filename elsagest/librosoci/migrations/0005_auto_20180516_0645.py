# Generated by Django 2.0.2 on 2018-05-16 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librosoci', '0004_auto_20180516_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='ruolo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='librosoci.Consigliere'),
            preserve_default=False,
        ),
    ]