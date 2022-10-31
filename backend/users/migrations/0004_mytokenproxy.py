# Generated by Django 3.2 on 2022-10-31 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0006_auto_20221031_1429'),
        ('users', '0003_alter_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTokenProxy',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authtoken.token')),
            ],
            options={
                'verbose_name': 'Токен',
                'verbose_name_plural': 'Токены',
            },
            bases=('authtoken.tokenproxy',),
        ),
    ]