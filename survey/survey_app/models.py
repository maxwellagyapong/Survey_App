from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Survey(models.Model):
    name = models.CharField(_("Survey Name"), max_length=255, unique=True)
    dt_created = models.DateTimeField(_("Date/Time Created"), auto_now_add=True,)
    dt_update = models.DateTimeField(_("Date/Time Updated"), auto_now=True)
    slug = models.SlugField(_("Slug"), blank=True, default="")
    
    def __str__(self) -> str:
        return self.name
