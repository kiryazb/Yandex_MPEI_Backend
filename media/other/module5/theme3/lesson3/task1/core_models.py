from django.db import models


class PublishedModel(models.Model):
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True
