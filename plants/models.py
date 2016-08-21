from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Plant(models.Model):
    plant_id = models.IntegerField(primary_key=True)
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    ca_native = models.CharField(max_length=5)

    def __str__(self):
        return '%s %s' % (self.plant_id, self.common_name)
    #name showing up at admin
    def __unicode__(self):
        return '%s' % self.common_name
    #the iten at database is able to be clicked on
    def get_scientific_name(self):
        return '%s' % self.scientific_name


class PlantPost(models.Model):
    post_id = models.TextField(primary_key=True)
    user_name = models.TextField(blank=True)
    user_id = models.TextField()
    post_date = models.DateField()
    photo_url = models.URLField()
    related_tag = models.TextField(blank=True)
    content = models.TextField(blank=True)
    geo_location = models.TextField(blank=True)
    post_link = models.URLField(max_length=255)
    plant = models.ForeignKey('Plant')
    score = models.IntegerField(blank=True)
    platform = models.CharField(max_length=10)

    def __str__(self):
        return '%s %s' % (self.post_id, self.plant.common_name)

    def __unicode__(self):
         return '%s' % (self.post_id)

class TaxonomyPost(models.Model):
    genus = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    post_id = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.genus, self.value)

    def __unicode__(self):
         return '%s' % (self.post_id)
#
# _SCORE_TYPE_CHOICES = (
#     (-1, 'DISLIKE'),
#     (1, 'LIKE'),
# )
#
# SCORE_TYPES = dict((value, key) for key, value in _SCORE_TYPE_CHOICES)
#
# class votingPost(models.Model):
#     post = model.ForeignKey('PlantPost')
#     rating = RatingField(can_change_vote=True)
#
#     def __str__(self):
#         return '%s %s' % (self.plant.common_name, self.rating)
