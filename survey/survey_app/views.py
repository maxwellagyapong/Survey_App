import json
from django.db import models
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
    template_name = "survey/SurveyDetail.html/"
    
    def get_object(self):
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
    
    def post(self, request: HttpRequest, *args: str) -> HttpResponse:
        survey_form = SurveyForm(request.POST or None)
        
        if survey_form.is_valid():
            messages.success(request,_("Survey successfully created."))
            
            survey = survey_form.save()
            return redirect("survey_detail", survey.slug)
        context = {
            "survey_form": survey_form,
        }

        return render(request, "survey/SurveyCreate.html", context)
    
    
def survey_update_view(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect('survey_list')

    survey_form = SurveyForm(request.POST or None, instance=survey)
    if survey_form.is_valid():
        messages.success(
            request,
            _("Survey successfully updated."))
        survey_form.save()
        return redirect("survey_list")

    context = {
        "survey": survey,
        "survey_form": survey_form,
    }

    return render(request, "survey/SurveyUpdate.html", context)


def survey_delete_view(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to delete does not exist."))
        return redirect("survey_list")

    survey.delete()
    messages.success(request, _("Survey has successfully deleted."))
    return redirect("survey_list")


def survey_result_view(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to delete does not exist."))
        return redirect("survey_list")

    try:
        results: list[SurveySubmission] = SurveySubmission.objects.filter(
            survey=survey)
    except SurveySubmission.DoesNotExist:
        results = None

    context = {
        "survey": survey,
        "results": results
    }

    return render(request, "survey/SurveyResult.html", context)


def survey_form_view(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to access does not exist."))
        return redirect("/")  # TODO

    context = {
        "survey": survey,
    }

    return render(request, "survey/SurveyForm.html", context)


def survey_form_submit_view(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "Can't submit survey, this survey is no longer active."))
        return redirect("/")  # TODO
    print(request.POST.dict())
    response = json.dumps(request.POST.dict(), indent=4)
    print(response)
    submission = SurveySubmission.objects.create(
        survey=survey,
        response=response,
    )
    submission.save()
    messages.success(request, _("Thank you for your submission."))
    return redirect("survey_form", survey.slug)  # TODO


def TextQuestionCreate(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to add question does not exist."))
        return redirect("survey_list")

    text_question_form = TextQuestionForm(request.POST or None)
    if text_question_form.is_valid():
        question = text_question_form.save()
        survey.add_question(question)
        messages.success(request, _(
            f"Question has successfully added to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "text_question_form": text_question_form
    }

    return render(request, "survey/TextQuestionCreate.html", context)    