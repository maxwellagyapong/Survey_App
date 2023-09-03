from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from survey_app import views
from survey_app.models import *

class TestUrls(SimpleTestCase):
    
    def test_survey_list_route(self):
        url = reverse("survey_list")
        url_view_function = resolve(url).func.view_class
        self.assertEqual(url_view_function, views.SurveyListView)

    def test_survey_create(self):
        url = reverse("survey_create")
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.survey_create_view)
        
        
class SurveyDetailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = Survey.objects.create(
            name="TestSurvey"
        )
        
    def test_survey_detail_route(self):
        url = reverse("survey_detail", args=[self.survey.slug])
        url_view_function = resolve(url).func.view_class
        self.assertEqual(url_view_function, views.SurveyDetailView)
        
    def test_survey_form_route(self):
        url = reverse("survey_form", args=[self.survey.slug])
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.survey_form_view)
        
    def test_survey_form_submit_route(self):
        url = reverse("survey_submit", args=[self.survey.slug])
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.survey_form_submit_view)
        
    def test_single_select_question_create_route(self):
        url = reverse("single_create", args=[self.survey.slug])
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.single_select_question_create)
        
class SingleSelectQuestionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = Survey.objects.create(
            name="TestSurvey"
        )
        
        cls.single_select_question = SingleSelectQuestion.objects.create(label='Will you?',
                                                                         is_required=True)
        
    def test_single_select_question_update(self):
        url = reverse("single_update", args=[self.survey.slug, self.single_select_question.pk])
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.single_select_question_update)
        
    def test_single_select_option_create(self):
        url = reverse("option_create", args=[self.survey.slug, self.single_select_question.pk])
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.single_select_option_create)
        
    def test_single_select_option_update(self):
        option = SingleSelectOptions.objects.create(select_question=self.single_select_question,
                                                    value='Yes.')
        url = reverse("options_update", args=[self.survey.slug, self.single_select_question.pk, option.pk])
        url_view_function = resolve(url).func
        self.assertEqual(url_view_function, views.single_select_option_update)