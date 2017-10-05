# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttagtype',
            name='project',
            field=models.ManyToManyField(to='project.TProject', blank=True),
        ),
        migrations.AlterField(
            model_name='tproject',
            name='project_tagname',
            field=models.ManyToManyField(to='project.ProjectTagType', blank=True),
        ),
    ]
