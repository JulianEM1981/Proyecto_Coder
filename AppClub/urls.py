from django.urls import path
from AppClub.views import *


urlpatterns = [
    path('', Inicio, name='inicio'),
    path('about/', sobremi, name="sobremi"),
    path('posts/publicados/', Publicados, name='publicados'),
    path('posts/publicados/<int:id>/', Post, name='post'),
    path('posts/nuevo/', Nuevo_posteo, name='nuevo_post'),
    path('editar_post/<int:id>/', Editar_post, name='editar_post'),
    path("posts/eliminar/<pk>/", Borrar_post.as_view(), name="eliminar_posts"),
    
  

]
