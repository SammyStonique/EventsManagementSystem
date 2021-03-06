# Generated by Django 3.1.6 on 2021-02-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventtype', models.CharField(choices=[('1', 'Public Event'), ('2', 'Invites Only')], default='Event Type', max_length=2)),
                ('eventname', models.CharField(max_length=100)),
                ('venue', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('guests', models.CharField(max_length=100)),
            ],
        ),
    ]
