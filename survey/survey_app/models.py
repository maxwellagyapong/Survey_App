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


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Survey"), 
                               on_delete=models.CASCADE, related_name="questions")
    question_content_type = models.ForeignKey(ContentType,
                            verbose_name=_("Question Content Type"),
                            on_delete=models.PROTECT)
    question_id = models.PositiveIntegerField(_("Question ID"))
    question = GenericForeignKey("question_content_type", "question_id")
    
    
