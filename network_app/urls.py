from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_person/', views.add_person, name='add_person'),
    path('add_connection/', views.add_connection, name='add_connection'),
    path('network/', views.view_network, name='view_network'),
    path('mock-network/', views.mock_view_network, name='mock_network'),
    path('add-sample-people/', views.add_sample_people, name='add_sample_people'),
]