# Generated by Django 3.1.7 on 2021-03-05 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0013_auto_20210305_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='createevent',
            name='created_by',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
