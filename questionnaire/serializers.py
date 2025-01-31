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
