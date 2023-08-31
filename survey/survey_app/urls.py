from django.urls import path, include
from .views import *

urlpatterns = [
    path('welcome/', SurveyListView.as_view(), name="survey_list"),
    path("create/", SurveyCreateView.as_view(), name="survey_create"),
    path("<slug:slug>/", include([
        path("", SurveyDetailView.as_view(), name="survey_detail"),
        path("update/", survey_update, name="survey_update"),
        path("delete/", survey_delete, name="survey_delete"),]))
]
