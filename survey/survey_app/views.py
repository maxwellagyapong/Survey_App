from typing import Any
from django.http import HttpRequest, HttpResponse
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
    template_name = "survey/SurveyList.html"
    
    
class SurveyDetailView(generic.DeleteView):
    template_name = "survey/SurveyDeatail.html/"
    
    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        
        if slug == None:
            messages.error(self.request, _(
            "The survey you are trying to access does not exist."))
            return redirect("survey_list")
            
        return Survey.objects.get(slug=slug)
    
    
class SurveyCreateView(generic.CreateView):
    template_name = "survey/SurveyCreate.html"
    queryset = Survey.objects.all()
    fields = ("name",)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        survey_form = SurveyForm(request.POST or None)
        
        if survey_form.is_valid():
            messages.success(request,_("Survey successfully created."))
            
            survey = survey_form.save()
            return redirect("survey_detail", survey.slug)
        context = {
            "survey_form": survey_form,
        }

        return render(request, "survey/SurveyCreate.html", context)
    