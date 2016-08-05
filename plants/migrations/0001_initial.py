# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 18:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('plant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('common_name', models.CharField(max_length=100)),
                ('scientific_name', models.CharField(max_length=100)),
                ('ca_native', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='PlantPost',
            fields=[
                ('post_id', models.TextField(primary_key=True, serialize=False)),
                ('user_name', models.TextField(blank=True)),
                ('user_id', models.TextField()),
                ('post_date', models.DateField()),
                ('photo_url', models.URLField()),
                ('related_tag', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('geo_location', models.TextField(blank=True)),
                ('post_link', models.URLField(max_length=255)),
                ('score', models.IntegerField(blank=True)),
                ('platform', models.CharField(max_length=10)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plants.Plant')),
            ],
        ),
        migrations.CreateModel(
            name='TaxonomyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genus', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('post_id', models.CharField(max_length=100)),
            ],
        ),
    ]
