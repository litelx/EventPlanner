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