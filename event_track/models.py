from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=10)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f'Event: {self.name}'
    

class BookedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booked_events')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_events')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} booked {self.event.name}'
    