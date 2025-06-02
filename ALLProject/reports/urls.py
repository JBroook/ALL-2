from django.urls import path
from . import views


appname = 'report'
urlpatterns = [
    path('sales/', views.ManagerReportView, name="sales"),
]