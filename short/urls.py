from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('link/', views.link, name='link'),
    path('link/', views.link, name='link'),
    path('link/<str:link_str>/', views.open_link, name='open_link'),
]
