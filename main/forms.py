from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Comment
from .models import Etkinlik
from django_recaptcha.fields import ReCaptchaField


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class EtkinlikForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Etkinlik
        fields = ['title', 'isActive', 'date', 'description', 'adress', 'category','enlem','boylam', 'image']
        widgets = {
            'enlem': forms.HiddenInput(),
            'boylam': forms.HiddenInput(),
        }
    def save(self, commit=True):
        instance = super(EtkinlikForm, self).save(commit=False)
        instance.slug = slugify(instance.title)  # Başlıktan slug oluştur
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = ['text', 'rate']
        widgets = {
            'rate': forms.HiddenInput(),
        }
