# Generated by Django 3.1.7 on 2021-03-05 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0010_auto_20210226_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestregistration',
            name='county',
            field=models.CharField(choices=[('-----', ''), ('Kisumu', 'Kisumu'), ('Nairobi', 'Nairobi'), ('Mombasa', 'Mombasa'), ('Siaya', 'Siaya')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='guestregistration',
            name='gender',
            field=models.CharField(choices=[('-----', ''), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='', max_length=100),
        ),
    ]
