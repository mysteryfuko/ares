# Generated by Django 3.0.7 on 2020-09-12 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noitces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('content', models.TextField()),
            ],
        ),
    ]