# Generated by Django 2.2.16 on 2023-02-04 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0002_auto_20230204_1702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donemaidate',
            options={'ordering': ['created']},
        ),
    ]
