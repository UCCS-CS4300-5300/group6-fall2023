# Generated by Django 4.2.6 on 2023-11-14 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('popularity_assessor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramaccount',
            name='id',
        ),
        migrations.AlterField(
            model_name='instagramaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
