from django import forms
from .models import (Survey, TextQuestion, NumberQuestion,
                    SingleSelectQuestion, SingleSelectOptions,)


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ("name",)