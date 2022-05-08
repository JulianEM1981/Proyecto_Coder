from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



#actualizar_usuario
class Usuario_registro(UserCreationForm):
    

    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput, )
    password2 = forms.CharField(label="Repetir contraseña",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = { k:"" for k in fields }
        
        
        
        
class Usuario_editar(UserCreationForm):
    
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)
    email = forms.EmailField(required=True)
    bio = forms.CharField(label="Descripción", required=True)
    web = forms.URLField(label="Sitio web", required=True)
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    
    def get_object(self):
        return self.request.user
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = { k:"" for k in fields }
   
    
        
    
class AvatarFormulario(forms.Form):
    
    imagen = forms.ImageField()
    
    
    
class Chats(forms.Form):
    
    mensaje = forms.CharField(max_length=200, label='')