from django.contrib import admin
from .models import Profile,CreateEvent,InvitedGuests

# Register your models here.
admin.site.register(Profile)
admin.site.register(CreateEvent)
admin.site.register(InvitedGuests)