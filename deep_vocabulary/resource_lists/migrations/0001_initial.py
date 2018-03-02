# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-18 04:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('secret_key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('cloned_from', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource_lists.ReadingList')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reading list',
            },
        ),
        migrations.CreateModel(
            name='ReadingListEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('cts_urn', models.CharField(max_length=250)),
                ('resource_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='resource_lists.ReadingList')),
            ],
            options={
                'verbose_name': 'reading list entry',
                'verbose_name_plural': 'reading list entries',
            },
        ),
        migrations.CreateModel(
            name='ReadingListSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('resource_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='resource_lists.ReadingList')),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reading list subscription',
                'verbose_name_plural': 'reading list subscriptions',
            },
        ),
        migrations.CreateModel(
            name='VocabularyList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('secret_key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('cloned_from', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource_lists.VocabularyList')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'vocabulary list',
            },
        ),
        migrations.CreateModel(
            name='VocabularyListEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('resource_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='resource_lists.VocabularyList')),
            ],
            options={
                'verbose_name': 'vocabulary list entry',
                'verbose_name_plural': 'vocabulary list entries',
            },
        ),
        migrations.CreateModel(
            name='VocabularyListSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('resource_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='resource_lists.VocabularyList')),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'vocabulary list subscription',
                'verbose_name_plural': 'vocabulary list subscriptions',
            },
        ),
    ]