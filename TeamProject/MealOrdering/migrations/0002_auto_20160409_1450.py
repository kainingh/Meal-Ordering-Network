# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchant',
            old_name='belonging',
            new_name='user',
        ),
    ]
