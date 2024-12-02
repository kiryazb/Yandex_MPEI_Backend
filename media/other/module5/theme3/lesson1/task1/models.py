from django.db import models


class Topping(models.Model):

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=64, unique=True)
    is_published = models.BooleanField(default=True)


class Wrapper(models.Model):

    title = models.CharField(max_length=256)
    is_published = models.BooleanField(default=True)


class IceCream(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField()
    is_on_main = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
