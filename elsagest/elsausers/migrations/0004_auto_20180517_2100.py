# Generated by Django 2.0.2 on 2018-05-17 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elsausers', '0003_auto_20180517_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailcredentials',
            old_name='e_resource',
            new_name='e_port',
        ),
        migrations.RenameField(
            model_name='emailcredentials',
            old_name='e_username',
            new_name='e_user',
        ),
    ]