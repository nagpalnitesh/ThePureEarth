# Generated by Django 4.1.5 on 2023-01-10 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pure', '0009_auto_20211115_1821'),
        ('orders', '0007_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pure.userauth'),
        ),
    ]
