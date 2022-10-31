# Generated by Django 3.2 on 2022-10-31 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0005_alter_token_options'),
        ('recipes', '0004_auto_20221028_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Токен',
                'verbose_name_plural': 'Токены',
                'abstract': False,
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('authtoken.token',),
        ),
    ]