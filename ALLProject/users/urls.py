from django.urls import path
from . import views

appname = 'users'
urlpatterns = [
    path('user_list/', views.user_list_view, name='user_list')
]
