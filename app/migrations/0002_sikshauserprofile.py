# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-01 11:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SikshaUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_picture', models.ImageField(upload_to='uploads/displaypictures')),
                ('gender', models.CharField(choices=[('U', 'Do Not Wish To Disclose'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
        ),
    ]
