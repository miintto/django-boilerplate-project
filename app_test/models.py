from django.db import models
from app_test import managers


class DumpModel(models.Model):
    contents_id   = models.BigAutoField(primary_key=True)
    contents_name = models.CharField(max_length=50)
    region        = models.CharField(max_length=20)
    address       = models.TextField()
    category      = models.CharField(max_length=20)
    price         = models.IntegerField()
    start_dtm     = models.DateTimeField()
    end_dtm       = models.DateTimeField()
    register_dtm  = models.DateTimeField(auto_now_add=True)

    objects = managers.DumpModelManager()

    class Meta:
        db_table = "tb__dump"
