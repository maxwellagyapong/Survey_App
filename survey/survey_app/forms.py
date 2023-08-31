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


class NumberQuestionForm(forms.ModelForm):

    class Meta:
        model = NumberQuestion
        fields = ("label", "is_required", "min_value", "max_value")
        
        
class SingleSelectQuestionForm(forms.ModelForm):

    class Meta:
        model = SingleSelectQuestion
        fields = ("label", "is_required",)
        
        
class SingleSelectOptionsForm(forms.ModelForm):

    class Meta:
        model = SingleSelectOptions
        fields = ("value",)
        
        
class ImageQuestionForm(forms.ModelForm):

    class Meta:
        model = TextQuestion
        fields = ("label", "is_required",)
        
        
class FileQuestionForm(forms.ModelForm):

    class Meta:
        model = TextQuestion
        fields = ("label", "is_required",)