from django.urls import path
from .import views
from .views import CreatePostView

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostsListView.as_view(), name='posts'),
    path('register/', views.Register, name='register'),
    path('create-post/', CreatePostView.as_view(), name='add_post'),
    path('personal-area/', views.MyDesign.as_view(), name='personal_area'),
    path('change-posts/', views.AdminListView.as_view(), name='change_post')
]
