from django.db import models

# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length=200)  # Foydalanuvchi ismi
    uid = models.CharField(max_length=1000)  # Foydalanuvchining UID (unique ID)
    room_name = models.CharField(max_length=200)  # Xona nomi
    insession = models.BooleanField(default=True)  # Sessiyada bormi

    def __str__(self):
        return self.name
