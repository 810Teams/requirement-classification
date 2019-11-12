from django.urls import path

from requirement import views

urlpatterns = [
    path('', views.index, name='index'),
]