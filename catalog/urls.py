from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostsListView.as_view(), name='posts'),
    path('register/', views.Register, name='register'),
]
