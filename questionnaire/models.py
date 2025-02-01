# models.py
from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Question(models.Model):
    questionid = models.AutoField(primary_key=True)
    trackid = models.IntegerField(null=True, blank=True)
    question = models.TextField(default="Default Question")
    correct_answer = models.TextField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)
    createdat = models.DateTimeField(default=timezone.now)
    option_a = models.TextField(null=True, blank=True)
    option_b = models.TextField(null=True, blank=True)
    option_c = models.TextField(null=True, blank=True)
    option_d = models.TextField(null=True, blank=True)
    next_question_id = models.IntegerField(null=True, blank=True)
    course_name = models.TextField(null=True, blank=True)
    q_level = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'questions'  # Set the table name for the database

    def __str__(self):
        return self.question


class Answer(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)  # Reference to User model
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Reference to Question model
    answer_text = models.TextField()  # Text of the user's answer
    is_correct = models.BooleanField(default=False)  # Whether the answer is correct
    answered_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the answer is submitted

    class Meta:
        db_table = 'useranswers'  # Set the table name for the database

    def __str__(self):
        return f"Answer for {self.question.question} by {self.user.username}"
