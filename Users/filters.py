import django_filters
from .models import *
from django_filters import CharFilter

class CreateEventFilter(django_filters.FilterSet):

    eventname = CharFilter(field_name='eventname',lookup_expr='icontains')
    venue = CharFilter(field_name='venue',lookup_expr='icontains')
    class Meta:
        model = CreateEvent
        fields = ['eventtype','eventname','venue']

class InvitedGuestsFilter(django_filters.FilterSet):

    guestname = CharFilter(field_name='guestname',lookup_expr='icontains')
    
    class Meta:
        model = InvitedGuests
        fields = ['guesttitle','guestname','guestrole']

class GuestRegistrationFilter(django_filters.FilterSet):

    firstname = CharFilter(field_name='firstname',lookup_expr='icontains')
    lastname = CharFilter(field_name='lastname',lookup_expr='icontains')
    
    class Meta:
        model = GuestRegistration
        fields = ['firstname','lastname','gender']

class InvitesOnlyRegistrationFilter(django_filters.FilterSet):

    firstname = CharFilter(field_name='firstname',lookup_expr='icontains')
    
    class Meta:
        model = InvitesOnlyRegistration
        fields = ['firstname','gender','reservation']

class GuestViewEventFilter(django_filters.FilterSet):

    eventname = CharFilter(field_name='eventname',lookup_expr='icontains')
    venue = CharFilter(field_name='venue',lookup_expr='icontains')
    class Meta:
        model = CreateEvent
        fields = ['created_by','eventname','venue']