# Generated by Django 3.0.6 on 2020-05-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('EUR', models.IntegerField()),
                ('USD', models.IntegerField()),
                ('JPY', models.IntegerField()),
                ('CNY', models.IntegerField()),
                ('EUR_n', models.IntegerField()),
                ('USD_n', models.IntegerField()),
                ('JPY_n', models.IntegerField()),
                ('CNY_n', models.IntegerField()),
            ],
        ),
    ]
