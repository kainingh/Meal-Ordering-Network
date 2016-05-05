# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0005_auto_20160409_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='rateNumber',
        ),
        migrations.RemoveField(
            model_name='dish',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='numberTotal',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='rateNumber',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='rating',
        ),
        migrations.AddField(
            model_name='customer',
            name='Address',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Address',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
