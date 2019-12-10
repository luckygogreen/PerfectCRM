from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout


# Create your views here.


def user_login(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET.get('next','/'))
        else:
            error_message = 'Wrong user or password!'
            return render(request, 'login.html',{'error_message':error_message})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/login/')
