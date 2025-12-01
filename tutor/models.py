from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    preferred_language = models.CharField(
        max_length=10, 
        choices=[
            ('en', 'English'),
            ('hi', 'Hindi'),
            ('es', 'Spanish'),
            ('fr', 'French'),
        ],
        default='en'
    )


class studentprofile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    topics_done = models.JSONField(default=list)
    progress_score = models.FloatField(default=0.0)
    interests = models.TextField()

class learningLog(models.Model):

    student = models.ForeignKey(studentprofile, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=255)
    explanation = models.TextField()
    quiz_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    quiz = models.TextField(blank=True, null=True)
    user_answers = models.TextField(blank=True, null=True)


# NCERT and Exam Pattern Models
class ClassLevel(models.Model):
    """Class/Grade levels (Class 1-12, competitive exams)"""
    class_name = models.CharField(max_length=50, unique=True)  # "Class 10", "JEE", "NEET", etc.
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.class_name
    
    class Meta:
        verbose_name_plural = "Class Levels"


class Subject(models.Model):
    """Subjects like Math, Physics, Chemistry, Biology, History, etc."""
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)  # "Mathematics", "Physics", "Biology"
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.class_level.class_name} - {self.name}"
    
    class Meta:
        unique_together = ('class_level', 'name')


class Topic(models.Model):
    """Topics within subjects (e.g., Algebra, Trigonometry for Math)"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"
    
    class Meta:
        unique_together = ('subject', 'name')


class AIQuestion(models.Model):
    """Questions asked by students to AI Tutor"""
    student = models.ForeignKey(studentprofile, on_delete=models.CASCADE, related_name='ai_questions')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    question_text = models.TextField()
    preferred_language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.question_text[:50]}"


class AIResponse(models.Model):
    """AI Tutor responses to questions"""
    question = models.OneToOneField(AIQuestion, on_delete=models.CASCADE, related_name='response')
    answer_text = models.TextField()
    language_provided = models.CharField(max_length=10, default='en')
    explanation = models.TextField(blank=True)
    follow_up_suggestions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to: {self.question.question_text[:50]}"


