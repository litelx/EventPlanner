from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


class GuestReponseForm(forms.Form):
    pass
    #
    # start = forms.DateTimeField(disabled=True)
    # end = forms.DateTimeField(disabled=True)
    # description = forms.Textarea(disabled=True)
    # location = forms.CharField(max_length=50)
