from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")


class AITutorService:
    """Service class to handle Gemini AI Tutor interactions with multi-language support"""
    
    MODEL_NAME = "gemini-2.5-flash"
    
    LANGUAGE_MAP = {
        'en': 'English',
        'hi': 'Hindi',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'pt': 'Portuguese'
    }
    
    @staticmethod
    def generate_ai_response(question_text, class_level, subject, topic, preferred_language='en'):
        """
        Generate AI response using Gemini 2.5 Flash
        
        Args:
            question_text: The student's question
            class_level: Class/Grade level (e.g., "Class 10")
            subject: Subject (e.g., "Mathematics")
            topic: Topic (e.g., "Algebra")
            preferred_language: Language code for response
        
        Returns:
            dict with answer, explanation, and follow-up suggestions
        """
        try:
            if not GEMINI_API_KEY:
                return {
                    'error': 'Gemini API key not configured',
                    'answer': 'Please configure Gemini API key in settings'
                }
            
            # Build contextual prompt
            system_prompt = f"""You are an expert AI Tutor specializing in NCERT curriculum and government exam preparation.
Your role is to help students understand academic concepts clearly and comprehensively.

Context:
- Class/Level: {class_level}
- Subject: {subject}
- Topic: {topic}

Instructions:
1. Provide clear, concise explanations suitable for the student's class level
2. Use examples and real-world applications when relevant
3. Explain step-by-step for complex concepts
4. Provide the answer in {AITutorService.LANGUAGE_MAP.get(preferred_language, 'English')}
5. At the end, suggest 2-3 follow-up topics the student can explore
6. Be encouraging and supportive

Question: {question_text}"""
            
            # Call Gemini API
            model = genai.GenerativeModel(AITutorService.MODEL_NAME)
            response = model.generate_content(system_prompt)
            
            answer_text = response.text if response else "Unable to generate response"
            
            # Extract follow-up suggestions
            follow_ups = AITutorService.extract_follow_ups(answer_text)
            
            return {
                'success': True,
                'answer': answer_text,
                'language': preferred_language,
                'follow_up_suggestions': follow_ups
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return {
                'error': str(e),
                'answer': f'Error generating response: {str(e)}'
            }
    
    @staticmethod
    def extract_follow_ups(response_text):
        """Extract follow-up topic suggestions from the response"""
        try:
            
            lines = response_text.split('\n')
            follow_ups = []
            
            for line in lines[-10:]:  # Check last 10 lines
                if any(char.isdigit() for char in line[:3]):
                    suggestion = line.strip()
                    if suggestion and len(suggestion) > 5:
                        follow_ups.append(suggestion)
            
            return follow_ups[:3]  # Return top 3
        except Exception:
            return []

def ShowLoginPage(request):
    return render(request, 'login.html')

def ShowRegisterPage(request):
    return render(request, 'register.html')

def ShowAITutorPage(request):
    return render(request, 'ai_tutor.html')

User = get_user_model()

class tutorAgent(APIView):
    """
    GET  -> render templates/tutor_ui.html (the HTML UI)
    POST -> existing behavior: call Gemini, store learningLog, return JSON
    """

    def get(self, request):
        # Render the static UI. Template should include:
        # <meta name="csrf-token" content="{{ csrf_token }}">
        return render(request, "tutor_ui.html")

    def post(self, request):
        topic = request.data.get('Topic')
        if not topic:
            return Response({'error': 'Topic is required.'}, status=status.HTTP_400_BAD_REQUEST)

        level = request.data.get('level', 'beginner')

        # generate explanation and quiz (your existing simple genai usage)
        expl_prompt = f"Explain {topic} to a {level} level student using simple examples"
        quiz_prompt = (
            f"Generate a 3-question multiple-choice quiz on {topic} for a {level} student. "
            "Return the result in valid JSON exactly as an array. Do not add extra text."
        )

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            explanation_resp = model.generate_content(expl_prompt)
            explanation = explanation_resp.text
        except Exception as e:
            return Response({'error': 'AI explanation failed', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            quiz_resp = model.generate_content(quiz_prompt)
            quiz_text = quiz_resp.text
            # try to parse JSON; if it fails we'll store raw text so you can inspect it
            try:
                quiz = json.loads(quiz_text)
            except Exception:
                quiz = quiz_text
        except Exception as e:
            return Response({'error': 'AI quiz failed', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # Only create/get a studentprofile for authenticated users
        if request.user and getattr(request.user, "is_authenticated", False):
            student_profile, _ = studentprofile.objects.get_or_create(user=request.user)
            student_field = student_profile
        else:
            student_field = None

        # create learning log (student can be null)
        learning_log = learningLog.objects.create(
            student=student_field,
            topic=topic,
            explanation=explanation,
            quiz_score=0,
            quiz=quiz
        )

        return Response({
            'topic': topic,
            'explanation': explanation,
            'quiz': quiz,
            'log_id': learning_log.id
        }, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class Register(APIView):
    permission_classes = []  # Allow anyone to register

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Debugging helper (optional)
        # print("Request data:", request.data)

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(username=username, password=password)
            return Response(
                {"message": "User created successfully.", "username": user.username},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"User creation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
class Login(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:

            return Response({"Error":"invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class SubmitQuiz(APIView):


    def post(self, request):

        log_id = request.data.get('log_id')
        answers = request.data.get('answers')

        try: 
            log = learningLog.objects.get(id=log_id, student__user = request.user)
        except learningLog.DoesNotExist:
            return Response({"message": "login not found"}, status=404)

        log.user_answers = answers
        log.quiz_score = self.evaluate_score(answers, log.quiz)
        log.save()

        return Response({"message": "Quiz submitted", "score": log.quiz_score})
    
    def evaluate_score(self, user_answers_json, quiz_json):

        try:
            user_answers = json.loads(user_answers_json)
            quiz = json.loads(quiz_json)
        except Exception:
            return 0
        
        score = 0

        for i, question in enumerate(quiz):

            correct = question.get("answer")
            user_answer = user_answers.get(str(i+1))

            if user_answer and user_answer.strip().upper() == correct.strip().upper():
                score+=1
        
        return score


# AI Tutor API Endpoints
class GetClassLevels(APIView):
    """Get all available class levels/grades"""
    permission_classes = []
    
    def get(self, request):
        try:
            classes = ClassLevel.objects.all().values('id', 'class_name', 'description')
            return Response({
                'success': True,
                'data': list(classes)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSubjects(APIView):
    """Get subjects for a specific class level"""
    permission_classes = []
    
    def get(self, request):
        class_id = request.query_params.get('class_id')
        
        if not class_id:
            return Response({'error': 'class_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subjects = Subject.objects.filter(class_level_id=class_id).values('id', 'name', 'description')
            return Response({
                'success': True,
                'data': list(subjects)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTopics(APIView):
    """Get topics for a specific subject"""
    permission_classes = []
    
    def get(self, request):
        subject_id = request.query_params.get('subject_id')
        
        if not subject_id:
            return Response({'error': 'subject_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            topics = Topic.objects.filter(subject_id=subject_id).values('id', 'name', 'description', 'difficulty_level')
            return Response({
                'success': True,
                'data': list(topics)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AskAITutor(APIView):
    """Ask a question to the AI Tutor"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            question_text = request.data.get('question')
            class_id = request.data.get('class_id')
            subject_id = request.data.get('subject_id')
            topic_id = request.data.get('topic_id')
            
            if not question_text:
                return Response({'error': 'Question text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get user's preferred language or use default
            user = request.user
            preferred_language = getattr(user, 'preferred_language', 'en')
            
            # Get class, subject, topic info
            class_level = None
            subject = None
            topic = None
            
            if class_id:
                class_level = ClassLevel.objects.filter(id=class_id).first()
            if subject_id:
                subject = Subject.objects.filter(id=subject_id).first()
            if topic_id:
                topic = Topic.objects.filter(id=topic_id).first()
            
            # Get or create student profile
            student_profile, _ = studentprofile.objects.get_or_create(user=user)
            
            # Create AI Question record
            ai_question = AIQuestion.objects.create(
                student=student_profile,
                class_level=class_level,
                subject=subject,
                topic=topic,
                question_text=question_text,
                preferred_language=preferred_language
            )
            
            # Generate AI response
            class_name = class_level.class_name if class_level else "General"
            subject_name = subject.name if subject else "General"
            topic_name = topic.name if topic else "General"
            
            ai_response_data = AITutorService.generate_ai_response(
                question_text=question_text,
                class_level=class_name,
                subject=subject_name,
                topic=topic_name,
                preferred_language=preferred_language
            )
            
            if 'error' in ai_response_data:
                return Response({
                    'error': ai_response_data['error'],
                    'question_id': ai_question.id
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Save AI Response
            ai_response = AIResponse.objects.create(
                question=ai_question,
                answer_text=ai_response_data.get('answer', ''),
                language_provided=preferred_language,
                follow_up_suggestions=ai_response_data.get('follow_up_suggestions', [])
            )
            
            return Response({
                'success': True,
                'question_id': ai_question.id,
                'response_id': ai_response.id,
                'answer': ai_response.answer_text,
                'follow_up_suggestions': ai_response.follow_up_suggestions,
                'language': preferred_language
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"AskAITutor error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetLanguagePreference(APIView):
    """Set user's preferred language for AI Tutor responses"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            language = request.data.get('language', 'en')
            
            if language not in AITutorService.LANGUAGE_MAP:
                return Response({
                    'error': f'Language not supported. Available: {list(AITutorService.LANGUAGE_MAP.keys())}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            user.preferred_language = language
            user.save()
            
            return Response({
                'success': True,
                'message': f'Language preference set to {AITutorService.LANGUAGE_MAP[language]}',
                'language': language
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetQuestionHistory(APIView):
    """Get user's question history with AI Tutor"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            student_profile = studentprofile.objects.filter(user=user).first()
            
            if not student_profile:
                return Response({'data': []}, status=status.HTTP_200_OK)
            
            questions = AIQuestion.objects.filter(student=student_profile).select_related('response').order_by('-created_at')[:20]
            
            data = []
            for q in questions:
                data.append({
                    'id': q.id,
                    'question': q.question_text,
                    'class_level': q.class_level.class_name if q.class_level else 'N/A',
                    'subject': q.subject.name if q.subject else 'N/A',
                    'topic': q.topic.name if q.topic else 'N/A',
                    'created_at': q.created_at.isoformat(),
                    'answer': q.response.answer_text if hasattr(q, 'response') and q.response else None
                })
            
            return Response({
                'success': True,
                'data': data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)