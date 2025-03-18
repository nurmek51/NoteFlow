from django.db import models
from ..users.models import User, StudyGroup

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='group_messages', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.group:
            return f'Group Message in {self.group.name} from {self.sender.username}'
        return f'Private Message from {self.sender.username} to {self.receiver.username}'
