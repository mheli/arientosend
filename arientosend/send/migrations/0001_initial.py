# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-07 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('key', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='FileAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.CharField(choices=[('P', 'Password'), ('U', 'User')], max_length=1)),
                ('password', models.CharField(max_length=30)),
                ('file_from_email', models.CharField(max_length=30)),
                ('file_sent_date', models.DateTimeField(editable=False)),
                ('file_expiration_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30, unique=True)),
                ('safenet_user', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='fileaccess',
            name='ariento_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='send.User'),
        ),
        migrations.AddField(
            model_name='fileaccess',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='send.File'),
        ),
    ]