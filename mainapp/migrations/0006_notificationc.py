# Generated by Django 4.2.7 on 2023-11-19 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_student_status'),
        ('mainapp', '0005_notifications_notificationp'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.professor')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.jobs')),
            ],
        ),
    ]
