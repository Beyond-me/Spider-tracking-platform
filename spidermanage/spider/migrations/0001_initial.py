# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DBname', models.CharField(max_length=50)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u6570\u636e\u5e93\u7c7b\u578b',
                'verbose_name_plural': '\u6570\u636e\u5e93\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.CharField(default=b'NULL', max_length=200)),
                ('content', models.CharField(default=b'NULL', max_length=200)),
                ('user', models.CharField(default=b'admin', max_length=100)),
            ],
            options={
                'verbose_name': '\u901a\u77e5',
                'verbose_name_plural': '\u901a\u77e5',
            },
        ),
        migrations.CreateModel(
            name='Spider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('spider_name', models.CharField(max_length=50)),
                ('spider_content', models.CharField(default=b'\xe6\x9a\x82\xe6\x97\xa0\xe6\x8f\x8f\xe8\xbf\xb0', max_length=200)),
                ('spider_url', models.CharField(default=b'url', max_length=200)),
                ('spider_request_count', models.IntegerField(default=0)),
                ('spider_download_count', models.IntegerField(default=0)),
                ('spider_info_count', models.IntegerField(default=0)),
                ('spider_error_count', models.IntegerField(default=0)),
                ('database_name', models.CharField(default=b'no info', max_length=50, null=True)),
                ('database_sheetname', models.CharField(default=b'no info', max_length=50, null=True)),
                ('spider_runing', models.BooleanField(default=False)),
                ('spider_runfunction', models.CharField(default=b'no info', max_length=50, null=True)),
                ('spider_runavg', models.CharField(default=b'no info', max_length=100, null=True)),
                ('spider_mark', models.CharField(default=b'no mark', max_length=200)),
                ('spider_pic', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('database_type', models.ForeignKey(blank=True, to='spider.DatabaseType', null=True)),
            ],
            options={
                'verbose_name': '\u722c\u866b',
                'verbose_name_plural': '\u722c\u866b',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='spider',
            field=models.ForeignKey(blank=True, to='spider.Spider', null=True),
        ),
    ]
