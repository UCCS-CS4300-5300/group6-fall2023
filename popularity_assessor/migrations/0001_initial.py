# Generated by Django 3.2.13 on 2023-11-09 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', django_cryptography.fields.encrypt(models.CharField(default=None, max_length=255))),
                ('previous_likes', models.IntegerField(default=0)),
                ('previous_followers', models.IntegerField(default=0)),
                ('previous_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
