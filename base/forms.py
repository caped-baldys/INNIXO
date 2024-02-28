from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Submission, User, Event , EventRegistration
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'name', 'email','bio', 'twitter', 'linkedin', 'facebook', 'github', 'website']    
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-field--input'}),
            'name':forms.TextInput(attrs={'class':'form-field--input'}),
            'email':forms.EmailInput(attrs={'class':'form-field--input'}),
            'bio':forms.Textarea(attrs={'class':'form-field--input-txarea'}),
            'twitter': forms.TextInput(attrs={'class':'form-field--input'}),
            'linkedin':forms.TextInput(attrs={'class':'form-field--input'}),
            'facebook':forms.TextInput(attrs={'class':'form-field--input'}),
            'github':forms.TextInput(attrs={'class':'form-field--input'}),
            'website':forms.TextInput(attrs={'class':'form-field--input'})
        }

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['details']
        
class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-field--input'}),
            'name':forms.TextInput(attrs={'class':'form-field--input'}),
            'email':forms.EmailInput(attrs={'class':'form-field--input'})
        }

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['team_name', 'phone_number', 'memeber_1', 'memeber_2', 'memeber_3', 'memeber_4', 'memeber_5', 'payment']
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'tel'}),
            'payment': forms.FileInput(attrs={'accept': 'image/*'}),
        }

        # def __init__(self, *args, **kwargs):
        #     super(EventRegistrationForm, self).__init__(*args, **kwargs)

        #     if self.instance and self.instance.pk:
        #         self.fields['event'].initial = self.instance.event

        #     member_count = self.instance.event.members_required
        #     # Attempt to get the event instance if it's already selected
        #     if 'instance' in kwargs and kwargs['instance']:
        #         event = kwargs['instance'].event
        #     elif 'initial' in kwargs and 'event' in kwargs['initial']:
        #         event = kwargs['initial']['event']

        #     if event:
        #         # Assume `members_required` is an attribute of the `Event` model indicating the number of members
        #         members_required = event.members_required
        #         for i in range(1, members_required + 1):
        #             field_name = f'member_{i}'
        #             self.fields[field_name] = forms.CharField(max_length=200, required=False, label=f'Member {i}')