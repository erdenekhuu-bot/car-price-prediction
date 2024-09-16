from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('estimate/', views.predict, name='predict-manufacturer'),
    path('predict_second/', views.predict_second, name='predict-category'),
    path('result/', views.result, name='result'),
    path('test/', views.upload, name='test'),
    path('predict/', views.predict, name='predict'),
    path('search', views.searchMark, name='search')
]