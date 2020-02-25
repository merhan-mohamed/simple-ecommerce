from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Profile
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #form.save()
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=password)
            user = form.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/product')

    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'Registration/signup.html', context)





@login_required(login_url='/accounts/login/')
def profile(request,slug):
    profile = get_object_or_404(Profile,slug=slug)
    return render(request, 'Registration/profile.html', {'profile':profile})
def logout(request):
    return render(request,'logged_out.html',{})
