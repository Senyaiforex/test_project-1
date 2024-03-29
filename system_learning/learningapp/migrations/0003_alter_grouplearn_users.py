# Generated by Django 5.0.2 on 2024-03-02 10:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningapp', '0002_alter_grouplearn_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplearn',
            name='users',
            field=models.ManyToManyField(related_name='groups_learn', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
    ]
