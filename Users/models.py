from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from multiselectfield import MultiSelectField
from PIL import Image

# Create your models here.
class Profile(models.Model):

    CITY = (('','Select your city'),('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Kisumu','Kisumu'))
    GENDER = (('','Select Gender'),('Male','Male'),('Female','Female'),('Other','Other')) 
    COUNTY = (('','Select County'),('Kisumu','Kisumu'),('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Siaya','Siaya'))
    RELIGION = (('','Select your Religion'),('Christian','Christian'),('Muslim','Muslim'),('Hindu','Hindu'),('Bahai','Bahai'),('Jew','Jew'))

    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=250)
    birthdate = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=250,choices=GENDER,default='')
    email = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    city = models.CharField(max_length=250,choices=CITY,default='')
    county = models.CharField(max_length=250,choices=COUNTY,default='')
    religion = models.CharField(max_length=250,choices=RELIGION,default='')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super(Profile,self).save()

        img = Image.open(self.image.path)

        if img.height > 20 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

class CreateEvent(models.Model):

    EVENTTYPE_CHOICES = (('','Select Event Type'),('Public Event', 'Public Event'),('Invites Only','Invites Only'))
    GUEST_LIST = (('','Select Gender'),('Dr.', 'Dr.'),('Sir','Sir'),('Madam','Madam'),('Mr.','Mr.'),('Mrs.','Mrs.'))
    
    eventtype = models.CharField(max_length=100,choices=EVENTTYPE_CHOICES,default='')
    eventname = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    date = models.DateField()
    guests = models.ManyToManyField('InvitedGuests')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.eventname}'

class InvitedGuests(models.Model):
    GUEST_TITLE = (('','Select Title'),('Dr.', 'Dr.'),('Sir','Sir'),('Madam','Madam'),('Mr.','Mr.'),('Mrs.','Mrs.'))
    GUEST_ROLE = (('','Select Role'),('Guest of Honour','Guest of Honour'),('Main Speaker','Main Speaker'),('Attendee','Attendee'))
    

    guesttitle = models.CharField(max_length=100,choices=GUEST_TITLE,default='')
    guestname= models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    identificationnumber = models.CharField(max_length=100)
    guestrole = models.CharField(max_length=100,choices=GUEST_ROLE,default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    contribution = models.CharField(max_length=100)

    def __str__(self):
        return self.guestname

class GuestRegistration(models.Model):
    GENDER = (('','Select Gender'),('Male','Male'),('Female','Female'),('Other','Other'))
    COUNTY = (('','Select County'),('Kisumu','Kisumu'),('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Siaya','Siaya'))
    
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    identificationnumber = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    gender = models.CharField(max_length=100,choices=GENDER,default='')
    county = models.CharField(max_length=100,choices=COUNTY,default='')
    event_organizer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    event_applied_for = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.firstname

class InvitesOnlyRegistration(models.Model):
    TITLE = (('','Select Title'),('Dr.', 'Dr.'),('Sir','Sir'),('Madam','Madam'),('Mr.','Mr.'),('Mrs.','Mrs.'))
    GENDER = (('','Select Gender'),('Male','Male'),('Female','Female'),('Other','Other'))
    COUNTY = (('','Select County'),('Kisumu','Kisumu'),('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Siaya','Siaya'))
    RESERVATION = (('','Select Reservation'),('VVIP','VVIP'),('VIP','VIP'),('Normal','Normal'))

    title = models.CharField(max_length=100,choices=TITLE,default='')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    identificationnumber = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    gender = models.CharField(max_length=100,choices=GENDER,default='')
    county = models.CharField(max_length=100,choices=COUNTY,default='')
    reservation = models.CharField(max_length=100, choices=RESERVATION,default='')
    event_organizer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    event_applied_for = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.firstname
