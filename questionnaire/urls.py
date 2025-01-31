from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import submit_answers

router = DefaultRouter()
# Register viewsets, not serializers
# router.register(r'questions', QuestionViewSet)  # Use the ViewSet for questions
# router.register(r'answers', AnswerViewSet)      # Use the ViewSet for answers

urlpatterns = [
    path('signup/questionnaire/questionnaire_view', views.questionnaire_view, name='questionnaire_view'),
    # path('questions/', views.quiz_questions_view, name='quiz_questions'),
    path('quiz_view', views.quiz_view, name='quiz_view'),
    path('quiz_form/questionnaire_completed/', views.questionnaire_completed, name='questionnaire_completed'),
    path('api/', include(router.urls)),  # Include the API routes for questions and answers
    # path('questions/', views.show_questions, name='show_questions'),
    path('api/submit-answers/', submit_answers,name='submit_answers'),
]
