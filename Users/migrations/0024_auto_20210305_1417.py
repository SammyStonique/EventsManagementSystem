# Generated by Django 3.1.7 on 2021-03-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_auto_20210305_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createevent',
            name='guests',
        ),
        migrations.AddField(
            model_name='createevent',
            name='guests',
            field=models.ManyToManyField(to='Users.InvitedGuests'),
        ),
    ]
