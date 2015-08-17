from django.contrib.auth.models import User
from django.contrib.gis.db import models
from jsonfield import JSONField
from geoq.core.models import AOI

class StoredTweet(models.Model):

    data = JSONField(null=False, blank=False, help_text='Tweet must be valid JSON')
    aoi = models.ForeignKey(AOI, blank=False, null=False)
    user = models.ForeignKey(User, blank=True, null=True)
    saved_at = models.DateTimeField(auto_now_add=True)
