from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from .models import Design
from .forms import UserRegistrationForm


# Create your views here.


def index(request):
    return render(
        request,
        'index.html',
        # context={'num_books': num_books, 'num_instances': num_instances,
        #          'num_instances_available': num_instances_available, 'num_authors': num_authors,
        #          'num_visits': num_visits},  # num_visits appended
    )


class PostsListView(generic.ListView):
    model = Design
    paginate_by = 4

    def get_queryset(self):
        ordering = self.request.GET.get('orderby')
        if ordering == 'Выполнено':
            ordering = 'ready'
        elif ordering == 'Принято в работу':
            ordering = 'load'
        elif ordering == 'Новая':
            ordering = 'new'
        elif ordering == 'Все':
            ordering = ''
        if ordering == '' or ordering == None:
            if self.request.user.is_staff:
                return Design.objects.filter()
            else:
                return Design.objects.filter(user__exact=self.request.user.id)
        else:
            if self.request.user.is_staff:
                return Design.objects.filter(status=ordering)
            else:
                return Design.objects.filter(user__exact=self.request.user.id, status=ordering)


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