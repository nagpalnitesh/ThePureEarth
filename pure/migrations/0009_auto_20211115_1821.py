# Generated by Django 3.2.9 on 2021-11-15 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pure', '0008_auto_20211115_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userauth',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='userauth',
            old_name='lastname',
            new_name='last_name',
        ),
    ]