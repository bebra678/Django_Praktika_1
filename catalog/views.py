from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .filters import CategoryFilters
from .models import Design, Category
from .forms import UserRegistrationForm, PostForm, CategoryForm, PostFormUpdateNew,\
    PostFormUpdateReady


# index
class IndexView(ListView):
    model = Design
    paginate_by = 4
    filter_class = CategoryFilters

    def get_queryset(self):
        return Design.objects.filter(status='ready')


class CategoryControl(ListView):
    model = Category
    template_name = 'catalog/category_control.html'


# создание постов
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Design
    form_class = PostForm
    template_name = 'catalog/create_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # super - функция, которая обращается к классу, от которого наследуется текущий.
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


# создание категории
class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/create_category.html'
    success_url = reverse_lazy('category_control')


# удаление заявок
class DeletePost(DeleteView):
    model = Design
    success_url = reverse_lazy('post_control')

    def form_valid(self):
        self.object.delete()


# удаление категорий
class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_control')
    template_name = 'catalog/delete_category.html'


# удаление заявок в личной кабинете
class DeletePostByUser(DeleteView, LoginRequiredMixin):
    model = Design
    success_url = reverse_lazy('personal_area')

    def form_valid(self):
        self.object.delete()


# обновление заявки
class PostUpdateNew(UpdateView):
    model = Design
    form_class = PostFormUpdateNew
    template_name = 'catalog/update_form_new.html'
    success_url = reverse_lazy('post_control')


# обновление заявки
class PostUpdateReady(UpdateView):
    model = Design
    form_class = PostFormUpdateReady
    template_name = 'catalog/update_form_ready.html'
    success_url = reverse_lazy('post_control')


# регистрация
def register(request):
    if request.user.id:
        return redirect('index')
    else:
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

#
# class SignUpView(CreateView):
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy('login')
#     template_name = 'register.html'


# логин
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('index.html')


# выход
def logout_view(request):
    logout(request)
    redirect('index.html')


# личный кабинет
@login_required
def my_post(request):
    f = CategoryFilters(request.GET, queryset=Design.objects.filter(user=request.user))
    return render(request, 'catalog/personal_area.html', {'filter': f})


# управления заявками
@staff_member_required(login_url='/accounts/login/')
def post_control(request):
    f = CategoryFilters(request.GET, queryset=Design.objects.all())
    return render(request, 'catalog/post_control.html', {'filter': f})

