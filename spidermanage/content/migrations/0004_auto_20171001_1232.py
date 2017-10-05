# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20171001_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articel_id',
            field=models.FloatField(default=1506832344.613323),
        ),
    ]
