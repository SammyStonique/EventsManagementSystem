# Generated by Django 3.1.7 on 2021-03-05 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0017_auto_20210305_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='createevent',
            old_name='event_organizer',
            new_name='created_by',
        ),
    ]
