from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import LoginForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if username == 'master' and password == 'keypass':
                request.session['is_authenticated'] = True
                return redirect('survey_list')  
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        
    context = {
        "form": form
    }
    
    return render(request, 'user/login.html', context)
