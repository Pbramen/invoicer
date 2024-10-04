from django.db import models

# Create your models here.
class File(models.Model):
    file_name = models.CharField( max_length=64)
    source = models.CharField(max_length=32, blank=True)
    extension = model.CharField(max_length=8)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)
    no_of_entries = models.IntegerField()

class ParserError(models.Model):
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    # TODO: Preview the format for antlr error (or design the custom error responses)

    