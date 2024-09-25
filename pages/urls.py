from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('estimate/', views.predict, name='predict-manufacturer'),
    path('car/', views.predict_second, name='predict-category'),
    path('predict/', views.predict, name='predict'),
    path('search', views.searchMark, name='search'),
    path('about_us/', views.about_us, name='about_us'),
    path('auth/login/',views.login, name='login'),
    path('auth/register/',views.signup, name='register'),
    path('auth/policy/', views.policy, name='policy'),
]