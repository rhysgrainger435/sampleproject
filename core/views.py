from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

from .forms import SignUpForm

def frontpage(request):
    return render(request, 'core/frontpage.html')


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect(profile)
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'core/profile.html', {'form': form})


@login_required
def profile_details(request):
    profile = request.user.profile
    return render(request, 'core/profile_detail.html', {'profile': profile})
