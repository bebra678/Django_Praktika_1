from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, TemplateView
from django_filters.views import FilterView
from .filters import CategoryFilters
from .models import Design, Category
from .forms import UserRegistrationForm, PostForm, CategoryForm


class IndexView(TemplateView):
    template_name = "index.html"


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Design
    form_class = PostForm
    template_name = 'catalog/create_post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        # super - функция, которая обращается к классу, от которого наследуется текущий.
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/create_category.html'
    success_url = reverse_lazy('post_control')


#FIXME: сменить def на class
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


#FIXME: lower word in def
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('index.html')


def logout_view(request):
    logout(request)
    redirect('index.html')


class PostsListView(ListView,):
    model = Design
    template_name = "catalog/design_list.html"
    paginate_by = 4
    filter_class = CategoryFilters

    def get_queryset(self):
        return Design.objects.filter(status='new')


def my_post(request):
    f = CategoryFilters(request.GET, queryset=Design.objects.filter(user=request.user))
    return render(request, 'catalog/personal_area.html', {'filter': f})


def post_control(request):
    f = CategoryFilters(request.GET, queryset=Design.objects.all())
    return render(request, 'catalog/post_control.html', {'filter': f})


class DeletePost(DeleteView):
    model = Design
    success_url = reverse_lazy('post_control')

    def form_valid(self):
        self.object.delete()


class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('post_control')

    def form_valid(self):
        self.object.delete()


class DeletePostByUser(DeleteView, LoginRequiredMixin):
    model = Design
    success_url = reverse_lazy('personal_area')

    def form_valid(self):
        self.object.delete()


class PostUpdate(UpdateView):
    model = Design
    fields = ('status', 'image', 'category', 'comment')
    template_name = 'catalog/update_form.html'
    success_url = reverse_lazy('post_control')

