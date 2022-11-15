from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .models import Design
from .forms import UserRegistrationForm, PostForm


# Create your views here.


def index(request):
    return render(
        request,
        'index.html',
    )


class PostsListView(generic.ListView):
    model = Design
    paginate_by = 4

    def get_queryset(self):

        return Design.objects.filter(status__exact='new').order_by('status')


class CreatePostView(CreateView): # new
    model = Design
    form_class = PostForm
    template_name = 'catalog/create_post.html'
    success_url = reverse_lazy('posts') # при удачном создании редирект к странице

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


def Register(request):
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


def My_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('index.html')
        ...
    else:
        pass


def Logout_view(request):
    logout(request)
    redirect('index.html')
    # Redirect to a success page.

