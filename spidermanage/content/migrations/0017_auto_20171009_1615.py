# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_auto_20171003_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articel_id',
            field=models.FloatField(default=1507536910.339643),
        ),
    ]
