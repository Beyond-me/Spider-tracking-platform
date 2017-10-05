# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('content', DjangoUeditor.models.UEditorField(default='', blank=True)),
                ('user', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u8bc4\u8bba',
                'verbose_name_plural': '\u9879\u76ee\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='ProjectTagType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagname', models.CharField(max_length=50)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u6807\u7b7e',
                'verbose_name_plural': '\u9879\u76ee\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=50)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u7c7b\u578b',
                'verbose_name_plural': '\u9879\u76ee\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='TProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=100)),
                ('project_url', models.CharField(max_length=200)),
                ('project_desc', DjangoUeditor.models.UEditorField(default='', blank=True)),
                ('project_mark', models.CharField(default=b'no mark', max_length=100)),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('project_shortnote', models.CharField(max_length=200)),
                ('isDelete', models.BooleanField(default=False)),
                ('project_tagname', models.ManyToManyField(to='project.ProjectTagType', null=True, blank=True)),
                ('project_type', models.ForeignKey(to='project.ProjectType')),
            ],
            options={
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
        ),
        migrations.AddField(
            model_name='projecttagtype',
            name='project',
            field=models.ManyToManyField(to='project.TProject', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(to='project.TProject'),
        ),
    ]
