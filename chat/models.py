from django.db import models
from accounts.models import User, InstitutionCode
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_code = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercode')
    recipient_code = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipientcode')
    create_at = models.DateTimeField(default=datetime.now())
    
    class Meta:
        db_table = 'room'
        
    def __str__(self):
        return f"{self.name}:{self.user_code}:{self.recipient_code}"
        
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user')
    message = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'message'
        ordering = ('-create_at', )        

    def __str__(self):
        return self.message
    