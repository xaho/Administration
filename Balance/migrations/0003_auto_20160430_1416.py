# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-30 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Balance', '0002_auto_20160228_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='Datum',
            new_name='Date',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Balance.Category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Balance.Store'),
        ),
    ]
