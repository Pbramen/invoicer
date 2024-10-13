from django.db import models
import re

class RemoveWS_Model(models.Model):
    class Meta:
        abstract = True 
    
    def save(self, *args, **kwargs):
        
        for field in self._meta.fields:
            if isinstance(field, models.CharField):
                value = getattr(self, field.name)
                if value is not None:
                    sub = re.sub(r'\s+', ' ', value).strip()
                    setattr(self, field.name, sub)
                    print(field.name, ':', sub)
        super(RemoveWS_Model, self).save(*args, **kwargs)