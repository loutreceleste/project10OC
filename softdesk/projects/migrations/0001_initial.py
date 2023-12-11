# Generated by Django 4.2.7 on 2023-12-11 18:20

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
            name='Comments',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(default=None, max_length=500)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('comments', models.ManyToManyField(blank=True, editable=False, related_name='contributor_comments', to='projects.comments')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('type', models.CharField(choices=[('BE', 'Back-end'), ('FE', 'Front-end'), ('IO', 'IOs'), ('AN', 'Android')], default=None, max_length=2)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('author', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_author', to='projects.contributor')),
                ('contributors', models.ManyToManyField(blank=True, related_name='project_contributors', to='projects.contributor')),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default=None, max_length=100, unique=True)),
                ('description', models.CharField(default=None, max_length=500)),
                ('priority', models.CharField(choices=[('LO', 'Low'), ('ME', 'Medium'), ('HI', 'High')], default=None, max_length=2)),
                ('nature', models.CharField(choices=[('BU', 'Bug'), ('FE', 'Feature'), ('TA', 'Task')], default=None, max_length=2)),
                ('progression', models.CharField(choices=[('TD', 'To-Do'), ('IP', 'In progress'), ('FI', 'Finished')], default='TD', max_length=2)),
                ('author', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to='projects.contributor')),
                ('projects', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_project', to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='contributor',
            name='issues',
            field=models.ManyToManyField(blank=True, editable=False, related_name='contributor_issues', to='projects.issues'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='contributor_projects', to='projects.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to='projects.contributor'),
        ),
        migrations.AddField(
            model_name='comments',
            name='issue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_issue', to='projects.issues'),
        ),
    ]
