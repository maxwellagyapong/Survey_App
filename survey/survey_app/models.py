from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Survey(models.Model):
    name = models.CharField(_("Survey Name"), max_length=255, unique=True)
    dt_created = models.DateTimeField(_("Date/Time Created"), auto_now_add=True,)
    dt_update = models.DateTimeField(_("Date/Time Updated"), auto_now=True)
    slug = models.SlugField(_("Slug"), blank=True, default="")
    
    def __str__(self) -> str:
        return self.name

    def add_question(self, question):
        question_content_type = ContentType.objects.get_for_model(question)
        return SurveyQuestion.objects.create(
            survey=self,
            question_content_type=question_content_type,
            question_id=question.pk
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Survey, self).save(*args, **kwargs)
    

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Survey"), 
                               on_delete=models.CASCADE, related_name="questions")
    question_content_type = models.ForeignKey(ContentType,
                            verbose_name=_("Question Content Type"),
                            on_delete=models.PROTECT)
    question_id = models.PositiveIntegerField(_("Question ID"))
    question = GenericForeignKey("question_content_type", "question_id")
    
    
class BaseQuestion(models.Model):
    label = models.CharField(_("Label"), max_length=255)
    is_required = models.BooleanField(_("Is Required?"))

    class Meta:
        abstract = True
        
        
class TextQuestion(BaseQuestion):
    input_length = models.PositiveIntegerField(_("Text Input Length"))
    
    
class NumberQuestion(BaseQuestion):
    min_value = models.FloatField(_("Minimum Value"))
    max_value = models.FloatField(_("Maximum Value"))
    
    
class SingleSelectQuestion(BaseQuestion):
    pass


class SingleSelectOptions(models.Model):
    select_question = models.ForeignKey(SingleSelectQuestion,
                        verbose_name=_("Single Select Question"),
                        on_delete=models.CASCADE, related_name="options")
    value = models.CharField(_("Value"), max_length=50)
    

class ImageQuestion(BaseQuestion):
    pass
    
    
class FileQuestion(BaseQuestion):
    pass
    
    
class SurveySubmission(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Survey"), 
                               on_delete=models.CASCADE, related_name="submissions")
    response = models.JSONField(_("Response"))
    dt_submission = models.DateTimeField(_("Date/Time Submission"), auto_now_add=True)