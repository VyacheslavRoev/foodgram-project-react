# Generated by Django 3.2 on 2022-10-27 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Подписка на пользователя', 'verbose_name_plural': 'Подписки на пользователей'},
        ),
    ]
