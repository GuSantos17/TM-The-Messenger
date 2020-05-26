from django.contrib import admin
from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login_us, name='login_us'),
    url(r'^logar', views.logar, name='logar'),
    url(r'^index', views.index, name='index'),
    url(r'^logout', views.logout_us, name='logout_us'),
    url(r'^register', views.register, name='register'),
    url(r'^recuperar_senha', views.recuperar_senha, name='recuperar_senha'),
    url(r'^find', views.index, name='find'),
    url(r'^friend', views.friend, name='friend'),
]
