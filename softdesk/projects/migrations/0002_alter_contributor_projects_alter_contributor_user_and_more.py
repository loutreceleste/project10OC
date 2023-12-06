# Generated by Django 4.2.7 on 2023-12-06 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='projects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributors_assigned', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='projects_contributed', to='projects.contributor'),
        ),
    ]
