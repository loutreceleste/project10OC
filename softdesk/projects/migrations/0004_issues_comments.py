# Generated by Django 4.2.7 on 2023-12-12 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_contributor_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='issues',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='issue_comments', to='projects.comments'),
        ),
    ]