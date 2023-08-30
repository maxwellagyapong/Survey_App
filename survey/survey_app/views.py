from django.contrib import admin
from .models import Survey, SurveySubmission
# Register your models here.


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    pass