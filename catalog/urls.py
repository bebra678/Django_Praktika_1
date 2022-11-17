from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.urls import path
from .import views
from .views import CreatePostView

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostsListView.as_view(), name='posts'),
    path('register/', views.Register, name='register'),
    path('create-post/', login_required(CreatePostView.as_view()), name='add_post'),
    path('personal-area/', login_required(views.MyDesign.as_view()), name='personal_area'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    path('post-control/', permission_required('change_post')(views.PostControl.as_view()), name='post_control'),
    path('delete-error/', views.get_error, name='error'),
]
