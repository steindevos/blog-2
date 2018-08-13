from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import ProfileRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, "profile_form": profile_form})