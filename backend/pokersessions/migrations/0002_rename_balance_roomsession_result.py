# Generated by Django 4.0.2 on 2022-03-14 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokersessions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomsession',
            old_name='balance',
            new_name='result',
        ),
    ]
