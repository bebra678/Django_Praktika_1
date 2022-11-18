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
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


#FIXME: сменить def на class
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


#FIXME: lower word in def
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('index.html')
    else:
        pass


def logout_view(request):
    logout(request)
    redirect('index.html')
    # Redirect to a success page.


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

    def form_valid(self, form):
        if self.object.status != 'new':
            return redirect('catalog/error_delete.html')
        else:
            self.object.delete()
            success_url = reverse_lazy('profile_applications')
            success_msg = 'Запись удалена'
            return HttpResponseRedirect(success_url, success_msg)


class PostControl(ListView):
    model = Design
    template_name = 'catalog/post_control.html'
    success_url = reverse_lazy('post_control')


class PostUpdate(UpdateView):
    model = Design
    fields = ('status', 'ready_images', 'category', 'comment')
    template_name = 'catalog/update_form.html'
    success_url = reverse_lazy('post_control')

    def get_context_data(self):
        context = super().get_context_data()
        if self.object.status == 'ready':
            context['is_ready'] = True
        elif self.object.status == 'load':
            context['is_load'] = True
        elif self.object.status == 'new':
            context['is_new'] = True
        return context
