from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from AppClub.models import Avatar
from AppClub.models import Posteos_nuevos
from Usuarios.models import Mensajes
from Usuarios.forms import Chats
from Usuarios.models import Perfil
from Usuarios.forms import Usuario_registro
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth import login, authenticate
from Usuarios.forms import Usuario_editar, AvatarFormulario


# Create your views here.


def Perfiles(request):
    
    posts = Posteos_nuevos.objects.filter(autor_id = request.user.id)
    
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(usuario = request.user)
    
        if len(avatar) > 0:
            imagen = avatar[0].img.url
            
            return render(request, 'Usuarios/perfil.html', {'imagen': imagen, 'posts': posts})
        
        else:
            return render(request, 'Usuarios/perfil.html')
            
    
@login_required(login_url='Usuarios/login/')
def actualizar_usuario(request):
    
    
    if request.method == 'POST':
        
        form = Usuario_editar(request.POST)
        
        
        if form.is_valid():
            
            data = form.cleaned_data
        
            
            
            perfil = Perfil.objects.get(usuario = request.user)
            
            perfil.nombre = data['first_name']
            perfil.apellido = data['last_name']
            perfil.email = data['email']
            perfil.bio = data['bio']
            perfil.web = data['web']
            
            perfil.save()
        
            
            return redirect('login_form')
        else: 
            return render(request, 'Usuarios/actualizar_usuario.html', {'form': form, 'mensaje': 'Formulario no válido'})
    else:
        form = Usuario_editar(initial={'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})

        
        return render(request, 'Usuarios/actualizar_usuario.html', {'form': form})
  
#login, registro
def login_form(request):
    
    if request.method == "POST":
        
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data
            
            username = data['username']
            contrasenia = data['password']
            
            user = authenticate(username=username, password=contrasenia)
            
            if user is not None:
                login(request, user)
                if request.user.is_authenticated:
                    avatar = Avatar.objects.filter(usuario = request.user)
    
                    if len(avatar) > 0:
                        imagen = avatar[0].img.url
                        return render(request, 'AppClub/inicio.html',{'imagen': imagen})
                    else:
                        return render(request, 'AppClub/inicio.html')
            else:
                return render(request, 'AppClub/login.html', {'form': formulario, 'mensaje': 'Usuario o contraseña incorrectos'})
        else:
            return render(request, 'AppClub/login.html', {'form': formulario, 'mensaje': 'Formulario no válido'})
    else:
        form = AuthenticationForm()
        return render(request, 'AppClub/login.html', {'form': form})


        
  
def registro(request):
    
    if request.method == "POST":
        form = Usuario_registro(request.POST)
        
        if form.is_valid():
            usuario = form.cleaned_data['username']
            form.save()
            
          
            user = Perfil( usuario = form.save(), email = form.cleaned_data['email'])
            user.save()
            
            
            
            return redirect('login_form')
        else:
            return render(request, 'Usuarios/registro.html', {'form': form, 'registraste': 'Formulario no válido'})
    else:
        form = Usuario_registro()
        return render(request, 'Usuarios/registro.html', {'form': form})

#avatars
@login_required(login_url='login/')
def cargar_avatar(request):

    
    if request.method == 'POST':
        formulario = AvatarFormulario(request.POST, request.FILES)
        
        if formulario.is_valid():
            usuario = request.user
            avatar = Avatar.objects.filter(usuario = usuario)
            
            if len(avatar) > 0:
                avatar = avatar[0]
                avatar.img = formulario.cleaned_data['imagen']
                avatar.save()
            else:
                avatar = Avatar(usuario = usuario, img = formulario.cleaned_data['imagen'])
                avatar.save()
        return redirect('inicio')
    else: 
           
                    
                formulario = AvatarFormulario()
                return render(request, 'Usuarios/cargar_imagen.html', {'form': formulario})
            
            
            
@login_required(login_url='login/')
def Mensajeria(request):
    
    
        Usuarios = Perfil.objects.exclude(usuario = request.user)
        
        return render(request, 'Usuarios/mensajes.html', {'Usuarios': Usuarios})

@login_required(login_url='login/')
def Chat(request, id):
    
    if request.user.is_authenticated:
        imagen = Avatar.objects.filter(usuario = request.user)
        if len(imagen) > 0:
            imagen = imagen[0].img.url
            
    
    if request.method == 'POST':
        
        form = Chats(request.POST)
        
        if form.is_valid():
            
            data = form.cleaned_data
          
            mensaje = Mensajes(emisor = request.user, destinatario = Perfil.objects.get(id = id), mensaje = data['mensaje'])
            mensaje.save()
            
            return redirect('chat', id)
        else:
            return render(request, 'Usuarios/chat.html', {'form': form, 'mensaje': 'Formulario no válido'})
    else:
        
        form = Chats()
        nombre = Perfil.objects.get(id = id)
        
        mensajes_recibidos = Mensajes.objects.filter(destinatario = request.user.username).filter(emisor = nombre.usuario).order_by('-fecha')
        
        mensajes_enviados = Mensajes.objects.filter(emisor_id = request.user.id, destinatario = nombre).order_by('-fecha')[:8]
    

        imagen_chat = Avatar.objects.filter(usuario = nombre.usuario)
        if len(imagen_chat) > 0:
            imagen_chat = imagen_chat[0].img.url

        return render(request, 'Usuarios/chat.html', {'id': id, 'form': form, 'nombre': nombre, 'mensajes_recibidos': mensajes_recibidos, 'mensajes_enviados': mensajes_enviados, 'imagen': imagen, 'imagen_chat': imagen_chat})