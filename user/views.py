from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


def home_view(request):
    return render(request, 'home.html')


@login_required()
def profile(request):
    return render(request, 'profile.html')


@csrf_protect
def custom_signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('account_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('account_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('account_signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = True  # Set user as active
        user.save()
        messages.success(request, 'Your account has been created. You can now log in.')
        return redirect('account_login')

    return render(request, 'account/signup.html')


@csrf_protect
def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password!')
            return redirect('account_login')

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('account_profile')  # Replace 'home' with your app's home URL

        messages.error(request, 'Invalid email or password!')
        return redirect('account_login')

    return render(request, 'account/login.html')


# Custom Logout View
@login_required
def custom_logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('account_login')


# Custom Forget Password View
# @csrf_protect
# def custom_forget_password_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password1 = request.POST['new_password']
#         password2 = request.POST['confirm_password']
#
#         if password1 != password2:
#             messages.error(request, 'Passwords do not match!')
#             return redirect('account_reset_password')
#
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request, 'Email not found!')
#             return redirect('account_reset_password')
#
#         user.set_password(password1)
#         user.save()
#         messages.success(request, 'Password reset successful! Please log in with your new password.')
#         return redirect('account_login')
#
#     return render(request, 'account/forget_password.html')
