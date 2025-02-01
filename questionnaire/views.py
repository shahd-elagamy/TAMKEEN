from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# def questionnaire_view(request):
#     # قائمة الأسئلة
#     questions = [
#         {"id": 1, "question": "Do you have any disability?", "options": ["Yes", "No"]},
#         {"id": 2, "question": "Do you have previous knowledge in CS?", "options": ["Yes", "No"]},
#         {"id": 3, "question": "What is your primary interest?", "options": ["Data Science", "Web Development", "AI"]},
#         {"id": 4, "question": "What is your level in the chosen track?", "options": ["Beginner", "Intermediate", "Advanced"]},
#     ]

#     # تعيين current_question_index إلى 0 إذا لم يكن موجودًا
#     if "current_question_index" not in request.session:
#         request.session["current_question_index"] = 0

#     # الحصول على المؤشر الحالي للسؤال
#     current_question_index = request.session["current_question_index"]

#     if request.method == "POST":
#         # حفظ الإجابة
#         answer = request.POST.get("answer")
#         if "answers" not in request.session:
#             request.session["answers"] = []
#         request.session["answers"].append({"question_id": questions[current_question_index]["id"], "answer": answer})

#         # تحديث المؤشر للسؤال التالي
#         request.session["current_question_index"] += 1
#         current_question_index = request.session["current_question_index"]

#     # التحقق من انتهاء الأسئلة
#     if current_question_index >= len(questions):
#         return render(request, "questionnaire/questionnaire_completed.html")

#     # إرسال السؤال الحالي للقالب
#     question = questions[current_question_index]
#     return render(request, "questionnaire/questionnaire_form.html", {"question": question})

from .models import Question

def questionnaire_view(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'questionnaire/questions_list.html', context)

# from django.shortcuts import render
# from .models import Question

# def quiz_view(request):
#     selected_track = request.GET.get('track', None)  # التراك الذي تم اختياره
#     if selected_track:
#         questions = Question.objects.filter(track__name=selected_track)  # فلترة الأسئلة بناءً على التراك
#     else:
#         questions = Question.objects.all()  # في حال لم يتم اختيار تراك، عرض جميع الأسئلة (أو يمكن إظهار رسالة خطأ)
# from django.shortcuts import render
from django.shortcuts import render

def questionnaire_completed(request):
    return render(request, 'questionnaire/questionnaire_completed.html')



# from django.shortcuts import render
# from .models import Question
# @login_required
# def quiz_view(request):
#     selected_interest = request.GET.get('interest')  # استرجاع التراك إذا كان يتم إرساله كمعامل
#     questions = Question.objects.filter(course_name=selected_interest)  # افترض أن لديك نموذج اسمه Question
#     return render(request, 'quiz_template.html', {'questions': questions})

from django.shortcuts import render
from .models import Question
from django.contrib.auth.decorators import login_required
import random

@login_required
def quiz_view(request):
    # Get the selected track (interest) from the request
    selected_interest = request.GET.get('interest')
    if not selected_interest:
        # If no interest is selected, return an empty questions list
        return render(request, 'quiz_template.html', {'questions': []})

    # Filter questions by the selected track (interest)
    all_questions = Question.objects.filter(course_name=selected_interest)

    # Separate questions by difficulty levels
    easy_questions = list(all_questions.filter(q_level='easy'))
    intermediate_questions = list(all_questions.filter(q_level='intermediate'))
    hard_questions = list(all_questions.filter(q_level='hard'))

    # Select a random set of questions based on the required distribution
    selected_questions = (
        random.sample(easy_questions, min(3, len(easy_questions))) +
        random.sample(intermediate_questions, min(4, len(intermediate_questions))) +
        random.sample(hard_questions, min(3, len(hard_questions)))
    )

    # Shuffle the selected questions to randomize their order
    random.shuffle(selected_questions)

    # Convert questions and options to lowercase
    for question in selected_questions:
        question.question = question.question.lower()
        question.option_a = question.option_a.lower()
        question.option_b = question.option_b.lower()
        question.option_c = question.option_c.lower()
        question.option_d = question.option_d.lower()

    # Render the questions to the template
    return render(request, 'quiz_template.html', {'questions': selected_questions})




from django.shortcuts import render
from .models import Question  # افترض أن الموديل هو Question

def quiz_view(request):
    track_id = request.GET.get('trackid')  # اجلب trackid من الـ GET request
    questions = Question.objects.filter(trackid=track_id)  # جلب الأسئلة بناءً على trackid
    return render(request, 'questionnaire/questions_list.html', {'questions': questions})

# from django.shortcuts import render
# from .models import Question

# def quiz_view(request):
#     # الحصول على trackid من الطلب (إذا لم يُرسل، يتم اعتباره None)
#     track_id = request.GET.get('trackid')

#     if track_id:
#         # جلب الأسئلة بناءً على trackid
#         questions = Question.objects.filter(trackid=track_id)
#     else:
#         # جلب جميع الأسئلة إذا لم يتم إرسال trackid
#         questions = Question.objects.all()

#     context = {
#         'questions': questions,
#     }
#     return render(request, 'questionnaire/questions_list.html', context)
# questionnaire/views.py
# views.py


# # عرض الصفحة التي تحتوي على الأسئلة
# def quiz_view(request):
#     questions = Question.objects.all()
#     return render(request, 'questionnaire/quiz_view.html', {'questions': questions})

# لحفظ الإجابات
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question, Answer
from .forms import AnswerForm
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required  # تأكد أن المستخدم مسجل الدخول
def submit_answers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', [])

            for answer_data in answers:
                question_id = answer_data.get('question_id')
                answer_text = answer_data.get('answer')

                # البحث عن السؤال
                try:
                    question = Question.objects.get(questionid=question_id)
                except Question.DoesNotExist:
                    return JsonResponse({'error': 'السؤال غير موجود!'}, status=400)

                # التحقق من صحة الإجابة
                is_correct = (answer_text == question.correct_answer)

                # إنشاء نموذج الإجابة وتعبئته
                form = AnswerForm({'question': question.id, 'answer_text': answer_text, 'is_correct': is_correct})

                if form.is_valid():
                    answer = form.save(commit=False)
                    answer.user = request.user  # ربط الإجابة بالمستخدم
                    answer.question = question  # تأكيد ربط السؤال بالإجابة
                    answer.save()
                else:
                    return JsonResponse({'error': 'نموذج الإجابة غير صالح!'}, status=400)

            return JsonResponse({'message': 'تم حفظ الإجابات بنجاح!'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'تنسيق JSON غير صالح!'}, status=400)

    return JsonResponse({'error': 'الطريقة غير مدعومة!'}, status=400)




# from rest_framework import viewsets
# from .models import Question, Answer
# from .serializers import QuestionSerializer, AnswerSerializer

# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()  # تحديد الـ queryset
#     serializer_class = QuestionSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import AnswerSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]  # تأكد من أن المستخدم مسجل الدخول

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # احفظ المستخدم المسجل حاليًا
