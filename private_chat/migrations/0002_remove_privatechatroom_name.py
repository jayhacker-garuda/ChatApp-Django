# Generated by Django 4.1.3 on 2022-11-30 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('private_chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatechatroom',
            name='name',
        ),
    ]
