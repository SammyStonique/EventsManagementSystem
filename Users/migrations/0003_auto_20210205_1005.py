# Generated by Django 3.1.6 on 2021-02-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_createevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitedGuests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guesttitle', models.CharField(choices=[('Dr.', 'Dr.'), ('Sir', 'Sir'), ('Madam', 'Madam'), ('Mr.', 'Mr.'), ('Mrs.', 'Mrs.')], default='', max_length=100)),
                ('guestname', models.CharField(max_length=100)),
                ('identificationnumber', models.CharField(max_length=100)),
                ('guestrole', models.CharField(choices=[('Guest of Honour', 'Guest of Honour'), ('Main Speaker', 'Main Speaker'), ('Attendee', 'Attendee')], default='', max_length=100)),
                ('contribution', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='createevent',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='createevent',
            name='eventtype',
            field=models.CharField(choices=[('Public Event', 'Public Event'), ('Invites Only', 'Invites Only')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='createevent',
            name='guests',
            field=models.IntegerField(),
        ),
    ]
