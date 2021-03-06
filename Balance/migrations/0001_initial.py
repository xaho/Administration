# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-14 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Find', models.CharField(max_length=255)),
                ('Replace', models.CharField(max_length=255)),
                ('Tags', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Store', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.DateTimeField()),
                ('Amount', models.FloatField()),
                ('Banknumber', models.CharField(max_length=255)),
                ('Description', models.CharField(max_length=255)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Balance.Category')),
                ('Store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Balance.Store')),
            ],
        ),
    ]
