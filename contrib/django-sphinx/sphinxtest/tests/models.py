from django.db import models

from djangosphinx import SphinxSearch

import datetime

class Group(models.Model):
    name = models.CharField(maxlength=32)

class Document(models.Model):
    group       = models.ForeignKey(Group)
    date_added  = models.DateTimeField(default=datetime.datetime.now)
    title       = models.CharField(maxlength=32)
    content     = models.TextField()
    
    search      = SphinxSearch(index="test")
    
    class Meta:
        db_table = 'documents'