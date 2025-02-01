# models.py
from django.db import models
from users.models import CustomUser

class Question(models.Model):
    questionid = models.AutoField(primary_key=True)
    trackid = models.IntegerField(null=True, blank=True)
    question = models.TextField()
    correct_answer = models.TextField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)
    createdat = models.DateTimeField(auto_now_add=True)
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
from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Answer(models.Model):
    answerid = models.AutoField(primary_key=True)  # AutoField for primary key
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='userid')  
    question = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='questionid')  
    answer = models.TextField(db_column='answer')  # Changed field name to 'answer' to match DB schema
    is_correct = models.BooleanField(default=False, db_column='iscorrect')  
    answered_at = models.DateTimeField(auto_now_add=True, db_column='answeredat')  

    class Meta:
        db_table = 'useranswers'  # Ensure table name matches the DB schema

    def __str__(self):
        return f"Answer for {self.question} by {self.userid}"  # Corrected user reference
