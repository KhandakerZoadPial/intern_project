# Generated by Django 4.2.7 on 2023-11-13 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_jobs_posted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='job_location',
            field=models.TextField(blank=True),
        ),
    ]
