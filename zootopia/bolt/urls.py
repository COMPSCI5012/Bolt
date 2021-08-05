from django.urls import path
from bolt import views

app_name = 'bolt'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shelter/<slug:shelter_name_slug>/',
          views.show_shelter, name='show_shelter'),
]