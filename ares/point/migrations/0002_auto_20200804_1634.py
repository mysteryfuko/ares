# Generated by Django 3.0.7 on 2020-08-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dkpadd',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='dkploot',
            name='time',
            field=models.DateTimeField(),
        ),
    ]