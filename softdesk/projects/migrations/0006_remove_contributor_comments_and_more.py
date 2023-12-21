# Generated by Django 5.0 on 2023-12-19 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_remove_project_contributors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='issues',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='projects',
        ),
        migrations.AddField(
            model_name='contributor',
            name='projects',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contributor_projects', to='projects.project'),
            preserve_default=False,
        ),
    ]
