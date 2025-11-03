from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, ForgotPasswordForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

@login_required
def homepage(request):
    return render(request, 'root.html')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'user/auth/app-auth-login-styled.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'user/auth/app-auth-login-styled.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('Form is valid')
            for field in form:
                print("Field: {}\nValue: {}".format(field.name, field.value()))
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'user/auth/app-auth-register-basic.html', {'form': form})
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = 'Password Reset Request'
            message = 'Please click the link below to reset your password.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'An email has been sent with instructions to reset your password.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'There was an error sending an email. Please try again later.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'user/auth/app-auth-password-basic.html', {'form': form})


#profile

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Account Successfully Created !!!')
            return redirect(reverse_lazy('profile'))
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'user/auth/app-auth-login-styled.html')


def test(request):
    return render(request, 'user/test.html')
