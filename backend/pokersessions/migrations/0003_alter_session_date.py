# Generated by Django 4.0.2 on 2022-03-14 07:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pokersessions', '0002_rename_balance_roomsession_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
