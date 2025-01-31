from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import submit_answers, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')  # استخدم ViewSet بدلاً من Serializer
router.register(r'answers', AnswerViewSet, basename='answer')        # استخدم ViewSet بدلاً من Serializer

urlpatterns = [
    path('signup/questionnaire/questionnaire_view', views.questionnaire_view, name='questionnaire_view'),
    path('quiz_view', views.quiz_view, name='quiz_view'),
    path('quiz_form/questionnaire_completed/', views.questionnaire_completed, name='questionnaire_completed'),
    path('api/', include(router.urls)),  # تضمين API المسارات الصحيحة
    path('api/submit-answers/', submit_answers, name='submit_answers'),
]
