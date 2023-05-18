from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView

from authentication.forms import UserRegisterForm, UserLoginForm


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'authentication/signup.html'

    def form_valid(self, form):
        user = User.objects.create_user(username=self.request.POST['username'],
                                        email=self.request.POST['email'],
                                        password=self.request.POST['password'])
        user.save()
        login(self.request, user)

        return redirect('home')

    def form_invalid(self, form):
        error = str(form.non_field_errors())[35: -10]
        context = {'form': form, 'error': error}
        return render(self.request, RegisterUser.template_name, context)


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'authentication/login.html'

    def form_valid(self, form):
        user = authenticate(
            self.request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password')
        )
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        error = str(form.non_field_errors())[35: -10]
        context = {'form': form, 'error': error}
        return render(self.request, LoginUser.template_name, self.get_context_data(**context))


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'authentication/logout.html')
    return redirect('login')
