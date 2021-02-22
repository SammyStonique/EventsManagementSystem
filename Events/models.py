from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Events(models.Model):
    eventtype = models.CharField(max_length=100)
    eventname = models.CharField(max_length=100)
    eventorganizer = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    guests = models.CharField(max_length=100)
    date = models.DateTimeField(editable=True)

    def __str__(self):
        return self.eventname