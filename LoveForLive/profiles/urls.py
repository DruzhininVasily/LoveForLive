from django.urls import path
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('account', views.account, name='account'),
    path('registration/', views.register, name='registration'),
    path('logout', views.logout_view, name='logout'),
    path('pass_reset/', authViews.PasswordResetView.as_view(template_name='profiles/pass_reset.html'), name='pass_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         authViews.PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_done/',
         authViews.PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_complete/',
         authViews.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'),
         name='password_reset_complete')
]