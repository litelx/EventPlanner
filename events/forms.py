from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


# class CreateEventForm(forms.Form):

    # start = forms.DateTimeField()
    # end = forms.DateTimeField()
    # description = forms.Textarea()
    # price = forms.DecimalField(1000000, 0, 10)
    # status = forms.CharField(max_length=10)
    #
    # location = forms.CharField(max_length=50)
    # location = forms.ForeignKey(Location, on_delete=models.CASCADE)