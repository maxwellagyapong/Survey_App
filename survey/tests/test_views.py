from django.test import TestCase
from django.urls import reverse
from user_app.models import User
from survey_app.models import *


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="testuser",
            password="password"
        )

    def test_survey_list_view(self):
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data)
        
        url = reverse("survey_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_survey_create_view(self):
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data)
        
        survey = {
            'name': 'testsurvey'
        }
        
        url = reverse("survey_create")
        response = self.client.post(url, survey, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_survey_update_view(self):
        
        survey = Survey.objects.create(name='testsurvey')
        
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data)
        
        newsurvey = {
            'name': 'testsurveyupdated'
        }
        
        url = reverse("survey_update", args=[survey.slug])
        response = self.client.put(url, newsurvey)
        self.assertEqual(response.status_code, 200)

    def test_survey_delete_view(self):
        
        survey = Survey.objects.create(name='testsurvey')
        
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data)        
        
        url = reverse("survey_update", args=[survey.slug])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        
        
    def test_single_select_question_create_view(self):
        
        survey = Survey.objects.create(name='testsurvey')
        
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data) 
        
        question = {
            'label':'Which of the following is true?', 
            'is_required':False
        }
        
        url = reverse('single_create', args=[survey.slug])
        response = self.client.post(url, question, follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_single_select_option_create_view(self):
        
        survey = Survey.objects.create(name='testsurvey')
        question = SingleSelectQuestion.objects.create(label='Which of the following is true?', 
                                               is_required=False)
        
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data) 
        
        option = {
            'value':'I am a boy.'
        }
        
        url = reverse('option_create', args=[survey.slug, question.id])
        response = self.client.post(url, option, follow=True)
        self.assertEqual(response.status_code, 200)   
        
    def test_single_select_option_update_view(self):
        
        survey = Survey.objects.create(name='testsurvey')
        question = SingleSelectQuestion.objects.create(label='Which of the following is true?', 
                                               is_required=False)
        option = SingleSelectOptions.objects.create(select_question=question, 
                                                    value='I am a boy.')
        
        data = {
            'username':'testuser',
            'password':'password'
        }
        
        self.client.post(reverse('login'), data) 
        
        newoption = {
            'value':'I am a girl.'
        }
        
        url = reverse('options_update', args=[survey.slug, question.id, option.id])
        response = self.client.put(url, newoption)
        self.assertEqual(response.status_code, 200)
        
    def test_survey_form_view(self):
        survey = Survey.objects.create(name='testsurvey')
        
        url = reverse('survey_form', args=[survey.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_survey_submit_view(self):
        survey = Survey.objects.create(name='testsurvey')
        
        submission = {
            'survey':survey,
            'response': {'question1': 'some answer', 'question2':'some answer 2'},
            'image': 'some image',
            'file': 'some file'
        }
        
        url = reverse('survey_submit', args=[survey.slug])
        response = self.client.post(url, submission, follow=True)
        self.assertEqual(response.status_code, 200)