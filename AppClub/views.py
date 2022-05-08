from random import random
from django.shortcuts import render, redirect
from AppClub.forms import Publicacion_nueva
from AppClub.models import *
from django.views.generic.edit import DeleteView

# Autenticacion Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.

def Inicio(request):
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(usuario = request.user)
    
        if len(avatar) > 0:
            imagen = avatar[0].img.url
    
            return render(request, 'AppClub/inicio.html', {'imagen': imagen})
        else:
            return render(request, 'AppClub/inicio.html')
    
    else:
        return render(request, 'AppClub/inicio.html')

def sobremi(request):
    dict_context = {"title" : "Sobre mi"}
    return render (request, "AppClub/sobremi.html", dict_context)


def Publicados(request):
    
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(usuario = request.user)
    
        if len(avatar) > 0:
            imagen = avatar[0].img.url
        else:
            imagen = ''
    else:
        imagen = ''
    
    posts = Posteos_nuevos.objects.all().order_by('-fecha')
    
    if request.method == 'GET':
        buscar = request.GET.get('buscar')
        if buscar:
            posts = Posteos_nuevos.objects.filter(titulo__icontains=buscar)
            
    
    return render(request, 'AppClub/publicados.html', {'posts': posts, 'imagen': imagen})

def Post(request, id):
    
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(usuario = request.user)
    
        if len(avatar) > 0:
            imagen = avatar[0].img.url
        else:
            imagen = ''
    else:
        imagen = ''
    
    post = Posteos_nuevos.objects.get(id=id)
    
    return render(request, 'AppClub/post.html', {'post': post, 'imagen': imagen})

@login_required(login_url='/login/')
def Nuevo_posteo(request): 
    
    
    if request.method == 'POST':
        
        posteo = Publicacion_nueva(request.POST, request.FILES)
        if posteo.is_valid():
            
            data = posteo.cleaned_data
            
            posteo_nuevo = Posteos_nuevos(titulo=data['titulo'],img=data['img'], post=data['post'], fecha=data['fecha'], autor=request.user)
   
            posteo_nuevo.save()
        
            return redirect('/posts/publicados/{}'.format(posteo_nuevo.id))
        else:
            return render(request, 'AppClub/publicacion_nueva.html', {'form': posteo, 'error': 'Formulario no válido'})
    else:
        posteo = Publicacion_nueva()
      
        
        return render(request, 'AppClub/publicacion_nueva.html', {'posteo': posteo, 'titulo': 'Escribir post', 'cta': 'Publicar'})
    

def Editar_post(request, id):
   
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(usuario = request.user)
    
        if len(avatar) > 0:
            imagen = avatar[0].img.url
        else:
            imagen = ''
            
        
    post_a_editar = Posteos_nuevos.objects.get(id=id)
    
    if request.method == 'POST':
        formulario_edicion = Publicacion_nueva(request.POST, request.FILES, instance=post_a_editar)
        if formulario_edicion.is_valid():
            
            data = formulario_edicion.cleaned_data
            
            post_a_editar.titulo = data['titulo']
            post_a_editar.post = data['post']
            
            post_a_editar.save()
            
            return render(request, 'AppClub/post.html', {'post': post_a_editar, 'imagen': imagen})
    
    
    else: 
        
        
        formulario = Publicacion_nueva(initial={'titulo': post_a_editar.titulo, 'post': post_a_editar.post, 'img': post_a_editar.img})
        
        return render(request, 'AppClub/publicacion_nueva.html', {'posteo': formulario,'titulo': "Editar", 'cta': "Confirmar cambios", 'imagen': imagen})

class Borrar_post(LoginRequiredMixin, DeleteView):
    
    model = Posteos_nuevos
    template_name = 'AppClub/borrar_post.html'
    success_url = '/posts/publicados/'

