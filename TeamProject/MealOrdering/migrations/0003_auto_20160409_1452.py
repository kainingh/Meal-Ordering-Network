# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0002_auto_20160409_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchant',
            old_name='user',
            new_name='belonging',
        ),
    ]
