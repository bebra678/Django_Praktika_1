from django.urls import path
from .import views
from .views import CreatePostView


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostsListView.as_view(), name='posts'),
    path('register/', views.Register, name='register'),
    path('create-post/', CreatePostView.as_view(), name='add_post')
]
