# Generated by Django 3.0.5 on 2020-05-09 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0004_staticfilepath'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_id', models.CharField(default='default', max_length=30)),
                ('datetime_stamp', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='CoinForTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_id', models.CharField(default='default', max_length=30)),
                ('coin_name', models.CharField(default='default', max_length=30)),
                ('datetime_stamp', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('price', models.FloatField(default=0.0)),
                ('percent_change_24h', models.FloatField(default=0.0)),
                ('percent_change_7d', models.FloatField(default=0.0)),
                ('percent_change_30d', models.FloatField(default=0.0)),
            ],
        ),
        migrations.DeleteModel(
            name='StaticFilePath',
        ),
    ]