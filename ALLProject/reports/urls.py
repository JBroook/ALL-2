from django.urls import path
from . import views


appname = 'report'
urlpatterns = [
    path('', views.ManagerReportView, name="report"),
    path('best-product', views.viewMoreBestProduct, name="bestProduct")
]