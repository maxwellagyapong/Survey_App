from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib import messages

def login_view(request):
    login_form = LoginForm(request.POST, None)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        
        if username is 'master' and password is 'keypass':
            request.session['is_authenticated'] = True
            messages.success(request, 'Welcome Survey Admin!')
            return redirect('survey_list')  
        else:
            messages.error(request, 'Invalid credentials. Please try again.') 
    
    context = {
        "login_form": login_form
    }
    
    return render(request, 'user/UserLogin.html', context)
