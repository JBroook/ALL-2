from django.urls import path
from . import views

appname = 'users'
urlpatterns = [
    path('user_list/', views.user_list_view, name='user_list'),
    path('user_list_partial/', views.user_list_partial_view, name='user_list_partial'),
    path('user_list_search/', views.user_list_search_view, name='user_list_search'),
    path('user_create/', views.user_create_view, name='user_create'),
]
