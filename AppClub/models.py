from django.db import models
from django.contrib.auth.models import User
from dataclasses import field
from ckeditor.fields import RichTextField

# Create your models here.


class Posteos_nuevos(models.Model):
    
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    img = models.ImageField(null=True)
    post = RichTextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)   
    
    def __str__(self) -> str:
        return f"Título: {self.titulo}"
     
    
class Avatar(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='avatar/', null=True, blank=True)