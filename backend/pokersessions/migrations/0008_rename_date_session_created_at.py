# Generated by Django 4.0.2 on 2022-03-18 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokersessions', '0007_alter_session_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='date',
            new_name='created_at',
        ),
    ]