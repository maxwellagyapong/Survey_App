from django.test import TestCase
from survey_app.models import *


class ModelTestCase(TestCase):
    
    def test_survey_model(self):
        survey = Survey.objects.create(name='testsurvey')
        
        self.assertTrue(Survey.objects.filter(id=survey.id).exists())
        
    def test_text_question_model(self):
        question = TextQuestion.objects.create(label='What is your name?', 
                                               is_required=True, input_length=10)
        
        self.assertTrue(TextQuestion.objects.filter(id=question.id).exists())
        
    def test_number_question_model(self):
        question = NumberQuestion.objects.create(label='How old are you?', 
                                               is_required=False, min_value=5, 
                                               max_value=100)
        
        self.assertTrue(NumberQuestion.objects.filter(id=question.id).exists())
        
    def test_single_select_question_model(self):
        question = SingleSelectQuestion.objects.create(label='Which of the following is true?', 
                                               is_required=False)
        
        self.assertTrue(SingleSelectQuestion.objects.filter(id=question.id).exists())
        
    def test_single_select_options_model(self):
        question = SingleSelectQuestion.objects.create(label='Which of the following is true?', 
                                               is_required=False)
        
        option = SingleSelectOptions.objects.create(select_question=question, 
                                                    value='I am a young man.')
        
        self.assertTrue(SingleSelectOptions.objects.filter(id=option.id).exists())
        
    def test_image_question_model(self):
        question = ImageQuestion.objects.create(label='Send me a new picture.', 
                                               is_required=False)
        
        self.assertTrue(ImageQuestion.objects.filter(id=question.id).exists())
        
    def test_file_question_model(self):
        question = FileQuestion.objects.create(label='Send your resume.', 
                                               is_required=True)
        
        self.assertTrue(FileQuestion.objects.filter(id=question.id).exists())
    
    def test_survey_submission_model(self):
        survey = Survey.objects.create(name='testsurvey')
        
        survey_submission = SurveySubmission.objects.create(survey=survey, 
                                                        response={'answer': '10'},
                                                        image='b',
                                                        file='c')
        
        self.assertTrue(SurveySubmission.objects.filter(id=survey_submission.id).exists())
    