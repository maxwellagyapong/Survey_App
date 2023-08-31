from django.urls import path, include
from .views import *

urlpatterns = [
    path('welcome/', SurveyListView.as_view(), name="survey_list"),
    path("create/", survey_create_view, name="survey_create"),
    path("<slug:slug>/", include([
        path("", SurveyDetailView.as_view(), name="survey_detail"),
        path("update/", survey_update_view, name="survey_update"),
        path("delete/", survey_delete_view, name="survey_delete"),
        path("result/", survey_result_view, name="survey_result"),
        
        path("text/", include([
            path("", text_question_create, name="text_create"),
            path("<int:id>", text_question_update, name="text_update"),])),
        
        path("number/", include([
            path("", number_question_create, name="number_create"),
            path("<int:id>/", number_question_update, name="number_update")])),
        
        path("single/", include([
            path("", single_select_question_create, name="single_create"),
            
            path("<int:id>/", include([
                path("", single_select_question_update, name="single_update"),
                path("option/", include([
                 path("", single_select_option_create, name="option_create"),
                 path("<int:option_id>/", single_select_option_update, 
                      name="options_update")]))
            ])),
        ])),
        
        path("image/", include([
            path("", image_question_create, name="image_create"),
            path("<int:id>", image_question_update, name="image_update"),])),
    ]))
]
