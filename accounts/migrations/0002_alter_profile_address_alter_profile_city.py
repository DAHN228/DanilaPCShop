# Generated by Django 4.1.5 on 2023-12-14 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(default='Lenina, 1', max_length=250),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Tomsk', max_length=100),
        ),
    ]
