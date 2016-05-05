# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0003_auto_20160409_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='belonging',
            new_name='user',
        ),
    ]
