from datetimewidget.widgets import DateTimeWidget
from django import forms
import events.models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())



class GuestForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()


class GuestReponseForm(forms.ModelForm):


    class Meta:
        model = events.models.Guest
        fields = ['status']
    status = forms.ChoiceField(label='Please respond', widget=forms.RadioSelect, choices=events.models.Guest.Status.choices[1:])

class EventForm(forms.ModelForm):

    class Meta:
        model = events.models.Event
        fields = (
            'title',
            'start',
            'end',
            'description',
            'price',
            'status',
            'location',
        )
    start = forms.DateTimeField(label='starts at', widget=DateTimeWidget(bootstrap_version=3, attrs={'data-readonly': 'false'}))
    end = forms.DateTimeField(label='ends at', widget=DateTimeWidget(bootstrap_version=3, attrs={'data-readonly': 'false'}))