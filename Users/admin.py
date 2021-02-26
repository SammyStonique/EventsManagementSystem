from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(CreateEvent)
admin.site.register(InvitedGuests)
admin.site.register(GuestRegistration)
admin.site.register(InvitesOnlyRegistration)