from cProfile import label
import datetime
from tabnanny import verbose
from django import forms
from django.contrib.auth.models import User
from AppClub.models import *
from ckeditor.widgets import CKEditorWidget


class Publicacion_nueva(forms.ModelForm):
    
    titulo = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}))
    img = models.ImageField(upload_to='img/')
    post = forms.CharField(widget=CKEditorWidget(), label='')
    fecha = forms.DateField(initial=datetime.datetime.today(), label='')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.titulo + ' | ' + self.autor.username
    
    class Meta:
        model = Posteos_nuevos
        fields = ['titulo', 'img', 'post']
        labels = {
            'post': '',
           
        }
        
    
        
        
        


