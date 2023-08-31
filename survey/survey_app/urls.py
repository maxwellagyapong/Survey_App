from django.urls import path
from .views import SurveyListView

urlpatterns = [
    path('welcome/', SurveyListView.as_view(), name="survey_list")
]
