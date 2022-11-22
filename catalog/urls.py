from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.urls import path
from .import views
from .views import CreatePostView, IndexView, CreateCategoryView

urlpatterns = [
    path('', IndexView.as_view(template_name="index.html"), name='index'),
    path('register/', views.register, name='register'),
    path('create-post/', CreatePostView.as_view(), name='add_post'),
    path('create-category/', CreateCategoryView.as_view(), name='add_category'),
    path('personal-area/', views.my_post, name='personal_area'),
    path('delete/<int:pk>/', permission_required('change_post')(views.DeletePost.as_view())
         , name='delete_post'),
    path('delete-category/<int:pk>/', permission_required('change_post')(
        views.DeleteCategoryView.as_view())
         , name='delete_category'),
    path('delete-by-user/<int:pk>/', views.DeletePostByUser.as_view(), name='delete_post_by_user'),
    path('post-control/', views.post_control, name='post_control'),
    path('category-control/',  staff_member_required(views.CategoryControl.as_view()),
         name='category_control'),
    path('update-post-new/<int:pk>/', permission_required('change_post')(
        views.PostUpdateNew.as_view())
         , name='update_form_new'),
    path('update-post-ready/<int:pk>/', permission_required('change_post')(
        views.PostUpdateReady.as_view())
         , name='update_form_ready'),
]
