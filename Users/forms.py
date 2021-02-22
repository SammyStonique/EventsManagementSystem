from django import forms
from django.forms import ModelForm
from .models import CreateEvent,InvitedGuests
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CreateEventForm(ModelForm):
    guests =forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          queryset=InvitedGuests.objects.all())
    class Meta:
        model = CreateEvent
        fields = ['eventtype','eventname','venue','description','date','guests']
        widgets = {
            'date' : DateInput()
        }
class InvitedGuestsForm(ModelForm):
    class Meta:
        model = InvitedGuests
        fields = ['guesttitle','guestname','email','identificationnumber','guestrole']
        help_texts = ''
        