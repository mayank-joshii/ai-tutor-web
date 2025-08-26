from .models import *
from .views import *
from .serializers import *
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/tutor', tutorAgent.as_view(), name='tutor-agent'),
    path('api/register/', Register.as_view(), name ='register'),
    path('api/login', Login.as_view(), name ='Login'),
    path('', ShowRegisterPage, name='registeration'),
    path('login.html/', ShowLoginPage, name='login'),
    path('api/submit-quiz', SubmitQuiz.as_view(), name='submit-quiz'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

