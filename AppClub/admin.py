from django.contrib import admin

from AppClub.views import Avatar, Posteos_nuevos
from .models import *


# Register your models here.
admin.site.register(Posteos_nuevos)
admin.site.register(Avatar)