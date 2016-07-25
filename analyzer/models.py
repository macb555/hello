from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class VisitorCounter(models.Model):
    visitor_name = models.CharField(max_length=15)
    visit_time = models.DateTimeField(default=timezone.now)
    visited_right_now = models.BooleanField(default=False)
    visited_page_url = models.CharField(default="/", max_length=100)
