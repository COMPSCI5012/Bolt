from django.urls import path
from bolt import views

app_name = 'bolt'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shelter/<slug:shelter_name_slug>/',
          views.show_shelter, name='show_shelter'),
    path('add_shelter/', views.add_shelter, name='add_shelter'),
    path('shelter/<slug:shelter_name_slug>/add_animal/', views.add_animal, name='add_animal'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('fqa/', views.fqa, name='fqa'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('myaccount/adoption_request/<int:request_pk>/<str:status>', views.adoption_request, name='adoption_request'),
    path('adoptions/', views.adoptions, name='adoptions'),
    path('adoptions/<str:animal_kind>', views.adoptions, name='adoptions'),
    path('adoptions/make_request/<int:animal_pk>', views.make_request, name='make_request')
]
