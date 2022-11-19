from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, TemplateView
from .models import Design
from .forms import UserRegistrationForm, PostForm


class IndexView(TemplateView):
    template_name = "index.html"


class PostsListView(ListView):
    model = Design
    paginate_by = 4

    def get_queryset(self):
        return Design.objects.filter(status='new')


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Design
    form_class = PostForm
    template_name = 'catalog/create_post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        # super - функция, которая обращается к классу, от которого наследуется текущий.
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


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


class MyDesign(LoginRequiredMixin, ListView):
    model = Design
    template_name = "catalog/personal_area.html"
    context_object_name = 'design_list'

    def get_queryset(self):
        queryset = Design.objects.filter(user=self.request.user)
        return queryset


class DeletePost(DeleteView):
    model = Design
    success_url = reverse_lazy('post_control')

    def form_valid(self):
        self.object.delete()


class DeletePostByUser(DeleteView):
    model = Design
    success_url = reverse_lazy('personal_area')

    def form_valid(self):
        self.object.delete()


class PostControl(ListView):
    model = Design
    template_name = 'catalog/post_control.html'


class PostUpdate(UpdateView):
    model = Design
    fields = ('status', 'image', 'category', 'comment')
    template_name = 'catalog/update_form.html'
    success_url = reverse_lazy('post_control')

