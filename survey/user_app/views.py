from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()

def login_view(request):
    login_form = LoginForm(request.POST, None)
    
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return redirect('survey_list')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
        # if username == 'master' and password == 'keypass':
        #     request.session['is_authenticated'] = True
        #     return redirect('survey_list')  
        # else:
        #     messages.error(request, 'Invalid credentials. Please try again.') 
    
    context = {
        "login_form": login_form
    }
    
    return render(request, 'user/UserLogin.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
