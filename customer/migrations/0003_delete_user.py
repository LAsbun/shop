# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20160407_1856'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
