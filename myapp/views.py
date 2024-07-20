from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,UserRegistrationForm
from .models import Menu


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
    return render(request, 'myapp/logout.html')

def register(request):
    if request.method =='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,'myapp/register_done.html')
    else:
        user_form = UserRegistrationForm()

    return render(request,'myapp/register.html',{'user_form':user_form})


