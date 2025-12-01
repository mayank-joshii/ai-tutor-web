from django.contrib import admin
from .models import (
    CustomUser, studentprofile, learningLog, 
    ClassLevel, Subject, Topic, AIQuestion, AIResponse
)

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'preferred_language', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('preferred_language', 'is_staff', 'is_active')


@admin.register(studentprofile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade', 'progress_score')
    search_fields = ('user__username',)


@admin.register(learningLog)
class LearningLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'quiz_score', 'created_at')
    search_fields = ('student__user__username', 'topic')
    list_filter = ('created_at', 'quiz_score')


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'description')
    search_fields = ('class_name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_level', 'description')
    search_fields = ('name', 'class_level__class_name')
    list_filter = ('class_level',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'difficulty_level')
    search_fields = ('name', 'subject__name')
    list_filter = ('difficulty_level', 'subject__class_level')


@admin.register(AIQuestion)
class AIQuestionAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_level', 'subject', 'topic', 'created_at')
    search_fields = ('student__user__username', 'question_text')
    list_filter = ('created_at', 'class_level', 'subject', 'preferred_language')
    readonly_fields = ('created_at',)


@admin.register(AIResponse)
class AIResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'language_provided', 'created_at')
    search_fields = ('question__question_text',)
    list_filter = ('language_provided', 'created_at')
    readonly_fields = ('created_at',)
