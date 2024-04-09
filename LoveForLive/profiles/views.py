from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, LoginForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Profile
from courses.models import Allowance


def create_profile(user_name):
    profile = Profile(user=user_name)
    profile.save()


def login_view(request):
    if request.method =="POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('account')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'profiles/login.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {user_name} был успешно создан!')
            user = User.objects.filter(username=user_name).first()
            create_profile(user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request,
                  'profiles/registration.html',
                  {
                      'title': 'Страница регистрации',
                      'form': form,
                  }
                  )


@login_required
def account(request):
    if request.method == "POST":
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен!')
            return redirect('account')

    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)
        Courses = Allowance.objects.filter(user=request.user).all()
    context = {
        'account': Profile.objects.filter(user=request.user).first(),
        'userForm': userForm,
        'updateForm': profileForm,
        'courses': Courses

    }
    return render(request, 'profiles/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')
