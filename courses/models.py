from django.conf import settings
from django.db import models


class Tracks(models.Model):
    name = models.CharField(max_length=255)  # اسم التراك
    description = models.TextField()  # وصف التراك

    class Meta:
        db_table = 'tracks'  # اسم الجدول في قاعدة البيانات


class Courses(models.Model):
    name = models.CharField(max_length=255)  # اسم الكورس
    description = models.TextField()  # وصف الكورس
    trackid = models.ForeignKey(
        Tracks, related_name='courses', on_delete=models.CASCADE, db_column='trackid'
    )  # ربط الكورس بالتراك، وتحديد اسم العمود في قاعدة البيانات
    level = models.CharField(max_length=50, default="Beginner")  # مستوى الكورس
    quiz_score = models.IntegerField(default=0)  # درجة الاختبار للمستخدم
    userid = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='userid',default=1
    )  # ربط الكورس بالمستخدم
    # created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإضافة
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # التقييم (0.00 إلى 5.00)

    class Meta:
        db_table = 'courses'  # اسم الجدول في قاعدة البيانات

    def __str__(self):
        return f"{self.name} - {self.level}"




from django.db import models
from django.utils import timezone
class playlist(models.Model):
    video_id = models.IntegerField(primary_key=True, default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(default="http://example.com")
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    duration = models.DurationField(default='1:00:00')
    difficultylevel = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner'
    )
    course = models.ForeignKey(Courses, related_name='playlists', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Ensure this field exists

    class Meta:
        db_table = 'playlist'

    def __str__(self):
        return self.name









# class Answer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # استخدام AUTH_USER_MODEL بدلاً من auth.User
#     course = models.ForeignKey(playlist, related_name='answers', on_delete=models.CASCADE)  # ربط الإجابة بالفيديو
#     question = models.CharField(max_length=255)  # السؤال الذي تم الإجابة عليه
#     answer = models.CharField(max_length=255)  # الإجابة على السؤال
#     disability_type = models.CharField(max_length=100, blank=True, null=True)  # نوع الإعاقة

#     class Meta:
#         db_table = 'useranswers'  

#     def __str__(self):
#         return f"{self.user.username} - {self.course.name} - {self.question}"


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey to User
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)  # ForeignKey to Course
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)  # ForeignKey to Track
    score = models.IntegerField()  # The score the user achieved
    quiz_date = models.DateTimeField(auto_now_add=True)  # Date when the quiz was taken

    class Meta:
        db_table = 'result'  # Name of the table in the database

    def __str__(self):
        return f"Result for {self.user.username} in {self.course.name} - {self.track.name}"
