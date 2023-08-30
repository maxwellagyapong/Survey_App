from django.contrib import admin
from .models import Survey, SurveySubmission


admin.site.register(Survey)
admin.site.register(SurveySubmission)