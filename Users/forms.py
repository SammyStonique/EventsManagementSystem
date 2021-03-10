from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(forms.Form):
    
    email = forms.EmailField()
    

    class Meta:
        model = User
        fields = ['username','password1','password2','image','bio','birthdate','gender','contact','city','county','religion']

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CreateEventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        self.user = kwargs.pop('user')
        super(CreateEventForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['guests'].required = False
        
        self.fields['guests'] =forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          queryset=InvitedGuests.objects.filter(created_by=self.user))
    
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

class GuestRegistrationForm(ModelForm):
    class Meta:
        model = GuestRegistration
        fields = ['firstname','lastname','email','identificationnumber','phonenumber','gender','county']   
        help_texts = ''

class InvitesOnlyRegistrationForm(ModelForm):
    class Meta:
        model = InvitesOnlyRegistration
        fields = ['title','firstname','lastname','email','identificationnumber','phonenumber','gender','county','reservation']   
        help_texts = ''

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio','birthdate','gender','contact','city','county','religion']
        widgets = {
            'birthdate' : DateInput()
        }
class UserUpdateForm(ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

