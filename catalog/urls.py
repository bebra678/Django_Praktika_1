from django.contrib.auth.decorators import permission_required
from django.urls import path
from .import views
from .views import CreatePostView, IndexView

urlpatterns = [
    path('', IndexView.as_view(template_name="index.html"), name='index'),
    path('posts/', views.PostsListView.as_view(), name='posts'),
    path('register/', views.register, name='register'),
    path('create-post/', CreatePostView.as_view(), name='add_post'),
    path('personal-area/', views.MyDesign.as_view(), name='personal_area'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete_post'),
    path('post-control/', permission_required('change_post')(views.PostControl.as_view()), name='post_control'),
    path('update-category/<int:pk>/', permission_required('change_post')(views.PostUpdate.as_view()), name='update_form'),
]
