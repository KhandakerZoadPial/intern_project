# Generated by Django 4.2.7 on 2023-11-19 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_student_status'),
        ('mainapp', '0006_notificationc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationp',
            old_name='professor',
            new_name='student',
        ),
        migrations.RemoveField(
            model_name='notificationc',
            name='company',
        ),
        migrations.AddField(
            model_name='notificationc',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.company'),
            preserve_default=False,
        ),
    ]
