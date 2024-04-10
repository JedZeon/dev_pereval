from django.db import models


class Added(models.Model):
    date_added = models.DateTimeField()
    raw_data = models.JSONField()
    images = models.JSONField()


class Areas(models.Model):
    id_parent = models.IntegerField(blank=False)
    title = models.TextField()


class Images(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='images/')


class Spr_Activities_Types(models.Model):
    title = models.TextField()
