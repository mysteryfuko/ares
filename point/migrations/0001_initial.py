# Generated by Django 3.0.7 on 2020-08-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DKPadd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('boss', models.TextField()),
                ('belong', models.IntegerField()),
                ('Player', models.TextField()),
                ('dkp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DKPLoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('item', models.IntegerField()),
                ('belong', models.IntegerField()),
                ('Player', models.TextField()),
                ('dkp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DKPtable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='epgp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.IntegerField(null=True)),
                ('ep', models.FloatField(blank=True, null=True)),
                ('gp', models.FloatField(blank=True, null=True)),
                ('time', models.DateTimeField()),
                ('boss', models.CharField(blank=True, max_length=40, null=True)),
                ('name', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='playerDKP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('job', models.CharField(default='WARRIOR', max_length=10)),
                ('dkp', models.IntegerField()),
                ('belong', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='playerEPGP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('job', models.CharField(default='WARRIOR', max_length=10)),
                ('ep', models.DecimalField(decimal_places=2, max_digits=8)),
                ('gp', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loading', models.TextField()),
                ('loadingNum', models.FloatField(max_length=5)),
                ('fight_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='xiaohao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dahao', models.CharField(max_length=20)),
                ('xiaohao', models.CharField(max_length=20)),
            ],
        ),
    ]
