from django.urls import path, include
from .views import *

urlpatterns = [
    path('welcome/', SurveyListView.as_view(), name="survey_list"),
    path("create/", SurveyCreateView.as_view(), name="survey_create"),
    path("<slug:slug>/", include([
        path("", SurveyDetail.as_view(), name="survey_detail"),]))
]
