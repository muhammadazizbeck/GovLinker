from django.forms import ModelForm
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import CustomUser



class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),max_length=50)

    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','age','city','region','countryside','password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Parollar mos emas!')
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput,max_length=50)

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Eski parol', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Yangi parol', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Yangi parolni tasdiqlang', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')  
        if not check_password(old_password, self.user.password):
            raise ValidationError('Eski parolingizni tekshirib qaytadan kiriting')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError('Parollar mos kelmadi')
        return cleaned_data




