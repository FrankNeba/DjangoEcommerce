from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, User



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['seller']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1','password2','username']

class UserUpdate(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'avatar', 'address', 'username']
