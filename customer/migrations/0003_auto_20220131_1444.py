# Generated by Django 3.2 on 2022-01-31 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20220131_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermodel',
            old_name='state',
            new_name='county',
        ),
        migrations.RenameField(
            model_name='ordermodel',
            old_name='city',
            new_name='town',
        ),
    ]
