from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('api/data', views.data, name='data'),
    path('api/send', views.send, name='send'),
    path('api/setup', views.setup, name='setup'),
    path('system_login', views.system_login, name='system_login'),

]