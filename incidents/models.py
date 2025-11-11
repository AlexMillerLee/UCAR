from django.db import models
from constans import incidents


class Incident(models.Model):
    incident = models.TextField()
    status = models.PositiveSmallIntegerField(choices=incidents.get_status(), default=0, db_index=True, )
    source = models.PositiveSmallIntegerField(choices=incidents.get_source(), default=3, db_index=True, )
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.incident[:30]}... ({self.get_status_display()})"
