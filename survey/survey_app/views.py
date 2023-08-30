from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import (Survey, SurveyQuestion, TextQuestion,
                    NumberQuestion, SingleSelectOptions,
                    SingleSelectQuestion, SurveySubmission,)
from .forms import *
from django.views import generic


class SurveyListView(generic.ListView):
    queryset = Survey.objects.all()
    template_name = ""
    
    
class SurveyDetailView(generic.DeleteView):
    template_name = ""
    
    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        
        if slug == None:
            messages.error(self.request, _(
            "The survey you are trying to access does not exist."))
            return redirect("survey_list")
            
        return Survey.objects.get(slug=slug)
    