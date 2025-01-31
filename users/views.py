from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm
from .models import CustomUser
from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")
            return redirect('questionnaire_view')  # Redirect to the questionnaire page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})







from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # تحقق من بيانات المستخدم
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # تسجيل الدخول للمستخدم
                return redirect('homepage')  # إعادة التوجيه إلى الصفحة الرئيسية باستخدام اسم الرابط
            else:
                messages.error(request, "wrong username or password")           
        else:
            messages.error(request, " Please enter correct username and password")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})




# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login page or any other page


# User API viewset (for REST framework)
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


from django.shortcuts import render

def dashboard_view(request):
    # Add any logic for the dashboard here (e.g., user data)
    return render(request, 'users/dashboard.html')  # The template for the dashboard


from django.http import JsonResponse
from .models import Track

def get_quiz_data(request):
    tracks = Track.objects.all()
    data = []
    for track in tracks:
        data.append({
            "name": track.name,
            "questions": [{"question_text": q.question_text} for q in track.questions.all()]
        })
    return JsonResponse(data, safe=False)
from django.http import JsonResponse
from .models import Track

def get_quiz_data(request):
    tracks = Track.objects.all()  # إحضار جميع الـ Tracks
    quiz_data = []
    
    for track in tracks:
        track_data = {
            'name': track.name,
            'questions': []
        }
        for question in track.questions.all():
            track_data['questions'].append({
                'id': question.id,
                'question_text': question.question_text
            })
        quiz_data.append(track_data)
    
    return JsonResponse(quiz_data, safe=False)

# views.py
from django.http import JsonResponse
from questionnaire.models import Question

def get_questions(request):
    track_name = request.GET.get('track', None)
    if track_name:
        questions = Question.objects.filter(track__name=track_name)
        data = [
            {"id": question.id, "text": question.question}
            for question in questions
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Track not provided"}, status=400)

# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer

class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# users/views.py
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


from django.http import JsonResponse
import json
from questionnaire.models import Answer
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def submit_quiz(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for item in data['answers']:
                Answer.objects.create(
                    user=request.user,
                    question_id=item['question_id'],
                    answer=item['answer']
                )
            return JsonResponse({"message": "Answers submitted successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


