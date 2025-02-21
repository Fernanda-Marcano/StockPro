from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.products.models import Value
from .models import Profile


class SignUpForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    """Form definition for Profile."""
    gender = forms.ModelChoiceField(queryset=Value.objects.filter(Q(hierar_id=13)), empty_label=None, label='Género', required=True, widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        """Meta definition for Profileform."""

        model = Profile
        fields = ('image',)
        labels = {
            'image':'Imagen de Perfil', 
        }


