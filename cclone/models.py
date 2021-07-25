from django.db import models
from django.utils import timezone

# Create your models here.
class Search(models.Model) :
    search_field = models.CharField(max_length = 200)
    time_created = models.DateTimeField(default = timezone.now)

    def __str__(self) :
            return self.search_field

    class Meta:
        verbose_name_plural = 'Searches'
