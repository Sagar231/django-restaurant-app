from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,UserRegistrationForm
from .models import Menu
from django.contrib import messages


# Create your views here.
def index(request):
    menu = Menu.objects.all()
    return render(request,'myapp/index.html',{"menu":menu})



def userlogin(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user= authenticate(request,
                               username = data['username'],
                               password=data['password']
                              )
            if user:
                login(request,user)
                return redirect('index')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    # return HttpResponse('cant show form')
    return render(request,'myapp/login.html',{'form':form})

def userlogout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'please fill the form correctly, choose different username and make sure your password matches')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'myapp/register.html', {'user_form': user_form})


