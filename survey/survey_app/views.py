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