# Generated by Django 4.1.4 on 2022-12-20 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_remove_contact_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
