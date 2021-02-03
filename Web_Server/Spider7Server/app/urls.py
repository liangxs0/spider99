from django.urls import path
from app import views

urlpatterns = [
    path("iplist", views.IPList.as_view(), name='iplist'),
]
