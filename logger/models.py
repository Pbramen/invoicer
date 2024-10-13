from django.db import models


# Create your models here.
class FileMeta(models.Model):
    pass
    # file_name = models.CharField(max_length=64)
    # version = models.IntegerField(default=0)
    # source = models.CharField(max_length=50, null=True)
    # extension = models.CharField(max_length=32)
    # file_size = models.FloatField(db_comment="in MB's")
    # checksum = models.CharField(max_length=255, null=True)

class ParserError(models.Model):
    pass

class SysError(models.Model):
    pass

class EndpointRequest(models.Model):
    pass