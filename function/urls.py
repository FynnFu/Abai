
from django.contrib import admin
from django.urls import path, include

from function.views import *

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('woe/', get_all_woe, name='woe'),
    path('ch/', get_all_ch, name='ch')
]
