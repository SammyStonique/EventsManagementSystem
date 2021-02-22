from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from multiselectfield import MultiSelectField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'



class CreateEvent(models.Model):

    EVENTTYPE_CHOICES = (('Public Event', 'Public Event'),('Invites Only','Invites Only'))
    GUEST_LIST = (('Dr.', 'Dr.'),('Sir','Sir'),('Madam','Madam'),('Mr.','Mr.'),('Mrs.','Mrs.'))
    
    eventtype = models.CharField(max_length=100,choices=EVENTTYPE_CHOICES,default='')
    eventname = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    date = models.DateField()
    guests = models.ManyToManyField('InvitedGuests')

    def __str__(self):
        return f'{self.eventname}'

class InvitedGuests(models.Model):
    GUEST_TITLE = (('Dr.', 'Dr.'),('Sir','Sir'),('Madam','Madam'),('Mr.','Mr.'),('Mrs.','Mrs.'))
    GUEST_ROLE = (('Guest of Honour','Guest of Honour'),('Main Speaker','Main Speaker'),('Attendee','Attendee'))

    guesttitle = models.CharField(max_length=100,choices=GUEST_TITLE,default='')
    guestname= models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    identificationnumber = models.CharField(max_length=100)
    guestrole = models.CharField(max_length=100,choices=GUEST_ROLE,default='')
    contribution = models.CharField(max_length=100)

    def __str__(self):
        return self.guestname
