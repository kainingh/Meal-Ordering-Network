# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0006_auto_20160410_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='Address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='Address',
            new_name='address',
        ),
    ]
