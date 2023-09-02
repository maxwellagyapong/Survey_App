import json
from django.db import models
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import (Survey, SurveyQuestion, TextQuestion,
                    NumberQuestion, SingleSelectOptions,
                    SingleSelectQuestion, SurveySubmission,)
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required


class SurveyListView(generic.ListView):
    queryset = Survey.objects.all()
    template_name = "survey/SurveyList.html"
    
    
class SurveyDetailView(generic.DeleteView):
    template_name = "survey/SurveyDetail.html/"
    
    def get_object(self):
        slug = self.kwargs.get('slug', None)
        
        if slug is None:
            messages.error(self.request, _(
            "The survey you are trying to access does not exist."))
            return redirect("survey_list")
            
        return Survey.objects.get(slug=slug)
    
@login_required
def survey_create_view(request):
    survey_form = SurveyForm(request.POST or None)
    if survey_form.is_valid():
        messages.success(
            request,
            _("Survey successfully created."))
        survey = survey_form.save()
        return redirect("survey_detail", survey.slug)
    context = {
        "survey_form": survey_form,
    }

    return render(request, "survey/SurveyCreate.html", context)
    
@login_required      
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

@login_required  
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

@login_required 
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
    response = json.dumps(request.POST.dict(), indent=4)
    # image = request.FILES['question.question.label']
    # file = request.FILES['question.question.label']
    print(response)
    submission = SurveySubmission.objects.create(
        survey=survey,
        response=response,
        # image = image,
        # file = file,
    )
    submission.save()
    messages.success(request, _("Thank you for your submission."))
    return redirect("survey_form", survey.slug)  # TODO

@login_required  
def text_question_create(request, slug):
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

@login_required  
def text_question_update(request, slug, id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    try:
        text_question: TextQuestion | None = TextQuestion.objects.filter(
            id=id).first()
    except TextQuestion.DoesNotExist:
        text_question = None

    if text_question is None:
        messages.error(request, _(
            "The question you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    text_question_form = TextQuestionForm(
        request.POST or None,
        instance=text_question
    )

    if text_question_form.is_valid():
        text_question_form.save()
        messages.success(request, _(
            f"Question has successfully updated to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "text_question": text_question,
        "text_question_form": text_question_form
    }

    return render(request, "survey/TextQuestionUpdate.html", context)

@login_required  
def number_question_create(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to add question does not exist."))
        return redirect("survey_list")

    number_question_form = NumberQuestionForm(request.POST or None)
    if number_question_form.is_valid():
        question = number_question_form.save()
        survey.add_question(question)
        messages.success(request, _(
            f"Question has successfully added to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "number_question_form": number_question_form
    }

    return render(request, "survey/NumberQuestionCreate.html", context)

@login_required  
def number_question_update(request, slug, id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you trying to update does not exist."))
        return redirect("survey_list")

    try:
        number_question: NumberQuestion | None = NumberQuestion.objects.filter(
            id=id).first()
    except NumberQuestion.DoesNotExist:
        number_question = None

    if number_question is None:
        messages.error(request, _(
            "The question you trying to update does not exist."))
        return redirect("survey_detail", slug)

    number_question_form = NumberQuestionForm(
        request.POST or None,
        instance=number_question
    )

    if number_question_form.is_valid():
        number_question_form.save()
        messages.success(request, _(
            f"Question has successfully update to survey {survey.name}."))
        return redirect("survey_detail", slug)
    
    context = {
        "survey": survey,
        "number_question": number_question,
        "number_question_form": number_question_form
    }

    return render(request, "survey/NumberQuestionUpdate.html", context)

@login_required  
def single_select_question_create(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    single_select_question_form = SingleSelectQuestionForm(
        request.POST or None)
    if single_select_question_form.is_valid():
        question = single_select_question_form.save()
        survey.add_question(question)
        messages.success(request, _(
            f"Question has successfully added to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "single_select_question_form": single_select_question_form,
    }

    return render(request, "survey/SingleSelectQuestionCreate.html", context)

@login_required  
def single_select_question_update(request, slug, id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    try:
        single_select_question: SingleSelectQuestion | None = SingleSelectQuestion.objects.filter(
            id=id).first()
    except SingleSelectQuestion.DoesNotExist:
        single_select_question = None

    if single_select_question is None:
        messages.error(request, _(
            "The question you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    single_select_question_form = SingleSelectQuestionForm(
        request.POST or None,
        instance=single_select_question
    )

    if single_select_question_form.is_valid():
        single_select_question_form.save()
        messages.success(request, _(
            f"Question has successfully update to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "single_select_question": single_select_question,
        "single_select_question_form": single_select_question_form
    }

    return render(request, "survey/SingleSelectQuestionUpdate.html", context)

@login_required  
def single_select_option_create(request, slug, id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    try:
        single_select_question: SingleSelectQuestion | None = SingleSelectQuestion.objects.filter(
            id=id).first()
    except SingleSelectQuestion.DoesNotExist:
        single_select_question = None

    if single_select_question is None:
        messages.error(request, _(
            "The question you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    single_select_options_form = SingleSelectOptionsForm(
        request.POST or None)
    if single_select_options_form.is_valid():
        options = single_select_options_form.save(commit=False)
        options.select_question = single_select_question
        options.save()
        messages.success(request, _(
            f"Option has successfully added to question."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "single_select_question": single_select_question,
        "single_select_options_form": single_select_options_form,
    }

    return render(request, "survey/SingleSelectOptionCreate.html", context)

@login_required  
def single_select_option_update(request, slug, id, option_id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    try:
        single_select_question: SingleSelectQuestion | None = SingleSelectQuestion.objects.filter(
            id=id).first()
    except SingleSelectQuestion.DoesNotExist:
        single_select_question = None

    if single_select_question is None:
        messages.error(request, _(
            "The question you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    try:
        option: SingleSelectOptions | None = SingleSelectOptions.objects.filter(
            id=option_id).first()
    except SingleSelectOptions.DoesNotExist:
        option = None

    if option is None:
        messages.error(request, _(
            "The option you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    single_select_options_form = SingleSelectOptionsForm(
        request.POST or None, instance=option)

    if single_select_options_form.is_valid():
        single_select_options_form.save()
        messages.success(request, _(
            f"Option has successfully updated."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "single_select_question": single_select_question,
        "option": option,
        "single_select_options_form": single_select_options_form
    }

    return render(request, "survey/SingleSelectOptionUpdate.html", context)

@login_required 
def image_question_create(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to add question does not exist."))
        return redirect("survey_list")

    image_question_form = ImageQuestionForm(request.POST or None)
    if image_question_form.is_valid():
        question = image_question_form.save()
        survey.add_question(question)
        messages.success(request, _(
            f"Question has successfully added to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "image_question_form": image_question_form
    }

    return render(request, "survey/ImageQuestionCreate.html", context)

@login_required  
def image_question_update(request, slug, id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    try:
        image_question: ImageQuestion | None = ImageQuestion.objects.filter(
            id=id).first()
    except ImageQuestion.DoesNotExist:
        image_question = None

    if image_question is None:
        messages.error(request, _(
            "The question you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    image_question_form = ImageQuestionForm(
        request.POST or None,
        instance=image_question
    )

    if image_question_form.is_valid():
        image_question_form.save()
        messages.success(request, _(
            f"Question has successfully updated to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "image_question": image_question,
        "image_question_form": image_question_form
    }

    return render(request, "survey/ImageQuestionUpdate.html", context)

@login_required  
def file_question_create(request, slug):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to add question does not exist."))
        return redirect("survey_list")

    file_question_form = FileQuestionForm(request.POST or None)
    if file_question_form.is_valid():
        question = file_question_form.save()
        survey.add_question(question)
        messages.success(request, _(
            f"Question has successfully added to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "file_question_form": file_question_form
    }

    return render(request, "survey/FileQuestionCreate.html", context)

@login_required  
def file_question_update(request, slug, id):
    try:
        survey: Survey | None = Survey.objects.filter(slug=slug).first()
    except Survey.DoesNotExist:
        survey = None

    if survey is None:
        messages.error(request, _(
            "The survey you are trying to update does not exist."))
        return redirect("survey_list")

    try:
        file_question: FileQuestion | None = FileQuestion.objects.filter(
            id=id).first()
    except FileQuestion.DoesNotExist:
        file_question = None

    if file_question is None:
        messages.error(request, _(
            "The question you are trying to update does not exist."))
        return redirect("survey_detail", slug)

    file_question_form = FileQuestionForm(
        request.POST or None,
        instance=file_question
    )

    if file_question_form.is_valid():
        file_question_form.save()
        messages.success(request, _(
            f"Question has successfully updated to survey {survey.name}."))
        return redirect("survey_detail", slug)

    context = {
        "survey": survey,
        "file_question": file_question,
        "file_question_form": file_question_form
    }

    return render(request, "survey/FileQuestionUpdate.html", context)    