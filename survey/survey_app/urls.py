from django.urls import path
from .views import *

urlpatterns = [
    path('welcome/', SurveyListView.as_view(), name="survey_list"),
    path("create/", SurveyCreateView.as_view(), name="survey_create"),
]
