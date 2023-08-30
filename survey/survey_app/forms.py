from django import forms
from .models import (Survey, TextQuestion, NumberQuestion,
                    SingleSelectQuestion, SingleSelectOptions,)


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ("name",)
        
        
class TextQuestionForm(forms.ModelForm):

    class Meta:
        model = TextQuestion
        fields = ("label", "is_required", "input_length",)
