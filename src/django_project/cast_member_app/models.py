from uuid import uuid4

from django.db import models


class CastMember(models.Model):
    app_label = "cast_member_app"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

    class Meta:
        db_table = 'cast_members'

    def __str__(self):
        return self.name
