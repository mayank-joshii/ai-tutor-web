from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
import json
from openai import OpenAI


# Create your views here.
def ShowLoginPage(request):
    return render(request, 'login.html')

def ShowRegisterPage(request):

    return render(request, 'register.html')

User = get_user_model()
client = OpenAI( base_url = "https://openrouter.ai/api/v1",
    api_key= "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")

class tutorAgent(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        topic = request.data.get('Topic')
        if not topic:
            return Response({'error': 'Topic is required.'}, status=400)
        level = request.data.get('level', 'beginner')
        explanation = self.get_ai_explanation(topic, level)
        quiz = self.generate_quiz(topic, level)

        student_profile, _ = studentprofile.objects.get_or_create(user=request.user)
        learning_log = learningLog.objects.create(
            student = student_profile,
            topic = topic,
            explanation = explanation,
            quiz_score = 0,
            quiz = quiz
        )

        

        return Response({'topic': topic, 'explanation': explanation,
                         'quiz': quiz, 'log_id': learning_log.id
                         })
    
    def get_ai_explanation(self, topic, level):

        prompt = f"Explain {topic} to a {level} level student using simple examples"

        response  = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages = [{'role':'user', 'content':prompt}]
            )

        return response.choices[0].message.content
    
    def generate_quiz(self, topic, level):
        prompt = f"""generate 3-question on {topic} for a {level} level student. Format the quiz in numbered questions
        Return the result in **valid JSON** with this format:
        
        [
        {{
            "question": "What is ...?",
            "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
            "answer": "B"
        }},
        ...
        ]
        """

        response  = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages = [{'role':'user', 'content':prompt}]
            )

        return response.choices[0].message.content

class Register(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({'detail': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():

            return Response ({"Error": "user already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password = password)

        return Response ({"Message": "User created successfully"}, status=status.HTTP_201_CREATED)
    
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

    permission_classes = [IsAuthenticated]

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
    


    