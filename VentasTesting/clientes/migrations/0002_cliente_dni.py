# Generated by Django 4.2.7 on 2024-10-09 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='dni',
            field=models.CharField(default=123, max_length=20),
        ),
    ]
