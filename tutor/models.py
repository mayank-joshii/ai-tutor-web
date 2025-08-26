from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class studentprofile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    topics_done = models.JSONField(default=list)
    progress_score = models.FloatField(default=0.0)
    interests = models.TextField()

class learningLog(models.Model):

    student = models.ForeignKey(studentprofile, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    explanation = models.TextField()
    quiz_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    quiz = models.TextField(blank=True, null=True)
    user_answers = models.TextField(blank=True, null=True)




    


