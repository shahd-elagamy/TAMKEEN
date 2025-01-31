# from rest_framework import serializers
# from .models import Question, Answer

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['questionid', 'trackid', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'course_name', 'q_level']

# class AnswerSerializer(serializers.ModelSerializer):
#     # Using the related questionid field as a nested serializer
#     questionid = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')

#     class Meta:
#         model = Answer
#         fields = ['userid', 'questionid', 'answer', 'is_correct']


from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['questionid', 'trackid', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'course_name', 'q_level']

class AnswerSerializer(serializers.ModelSerializer):
    questionid = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), 
        source='question'
    )
    is_correct = serializers.BooleanField(read_only=True)  # اجعل `is_correct` للقراءة فقط

    class Meta:
        model = Answer
        fields = ['userid', 'questionid', 'answer', 'is_correct']

    def validate(self, data):
        """
        التحقق من صحة الإجابة بمقارنتها بالإجابة الصحيحة للسؤال.
        """
        question = data['question']
        if data['answer'].lower() != question.correct_answer.lower():
            data['is_correct'] = False
        else:
            data['is_correct'] = True
        return data
