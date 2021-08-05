from django.urls import path
from bolt import views

app_name = 'bolt'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shelter/<slug:shelter_name_slug>/',
          views.show_shelter, name='show_shelter'),
    path('add_shelter/', views.add_shelter, name='add_shelter'),
    path('shelter/<slug:shelter_name_slug>/add_animal', views.add_animal, name='add_animal'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('fqa/', views.fqa, name='fqa'),
]