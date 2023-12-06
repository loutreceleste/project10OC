# Generated by Django 4.2.7 on 2023-12-06 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BE', 'Back-end'), ('FE', 'Front-end'), ('IO', 'IOs'), ('AN', 'Android')], default=None, max_length=2)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('contributors', models.ManyToManyField(blank=True, related_name='contributors', to='projects.contributor')),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_author', to=settings.AUTH_USER_MODEL)),
                ('projects', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='contributor',
            name='projects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to=settings.AUTH_USER_MODEL),
        ),
    ]