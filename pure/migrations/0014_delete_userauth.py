# Generated by Django 4.1.5 on 2023-01-19 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_user'),
        ('pure', '0013_profile_auth_token_profile_forget_password_token_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAuth',
        ),
    ]
