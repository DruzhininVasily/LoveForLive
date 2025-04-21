from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, LoginForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Profile
from courses.models import Allowance


def create_profile(user_name, phone):
    profile = Profile(user=user_name, phone=phone)
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
        profile_form = ProfileUpdateForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            phone = profile_form.cleaned_data.get('phone')
            user_name = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {user_name} был успешно создан!')
            user = User.objects.filter(username=user_name).first()
            create_profile(user, phone)
            return redirect('home')
    else:
        form = UserRegisterForm()
        profile_form = ProfileUpdateForm

    return render(request,
                  'profiles/registration.html',
                  {
                      'title': 'Страница регистрации',
                      'form': form,
                      'profile_form': profile_form
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
        print(Courses)
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
