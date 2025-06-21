from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

appname = 'users'
urlpatterns = [
    path('user_list/', views.user_list_view, name='user_list'),
    path('user_list_partial/', views.user_list_partial_view, name='user_list_partial'),
    path('user_list_search/', views.user_list_search_view, name='user_list_search'),
    path('user_create_form/', views.user_create_form_view, name='user_create_form'),
    path('user_create/', views.user_create_view, name='user_create'),
    path('user_info/<int:employee_id>/', views.user_info_view, name='user_info'),
    path('user_edit_form/<int:employee_id>/', views.user_edit_form_view, name='user_edit_form'),
    path('user_edit/<int:employee_id>/', views.user_edit_view, name='user_edit'),
    path('user_delete/<int:employee_id>/', views.user_delete_view, name='user_delete'),
    path('home/', views.home_view, name='home'),
    path('user_logout/', views.logout_view, name='user_logout'),
    path('user_login/', views.CustomLoginView.as_view(), name='user_login'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name = 'users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
