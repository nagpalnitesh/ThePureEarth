# Generated by Django 3.2.9 on 2021-11-11 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauth',
            name='is_Verified',
            field=models.BooleanField(default=False),
        ),
    ]
