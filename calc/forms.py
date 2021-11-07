from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Bus
class BookForm(forms.Form):
    from_data=forms.CharField(max_length=200)
    to_data=forms.CharField(max_length=200)

    class Meta:
        model = Bus
        fields = ('from_data', 'to_data')


class UserForm(UserCreationForm):
    first_name=forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number=forms.IntegerField()

    class Meta:
        model=User
        fields=('first_name','last_name','username','email','password1','password2','phone_number')



