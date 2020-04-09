from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    name = models.CharField(max_length=200,unique=True)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    code=models.CharField(max_length=12,unique=True)
    description=models.TextField()
    time_limit=models.PositiveIntegerField(help_text='In Minuts')
    total_questions=models.PositiveIntegerField(help_text="Must be less than 10")
    passing_marks=models.PositiveIntegerField(help_text='Must be less than 100')
    marks_per_question=models.PositiveIntegerField()
    def __str__(self):
        return self.name
class Question(models.Model):
    ANS =( 
        ("A", "A"), 
        ("B", "B"), 
        ("C", "C"), 
        ("D", "D"), 
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_A=models.CharField(max_length=200)    
    option_B=models.CharField(max_length=200)    
    option_C=models.CharField(max_length=200)    
    option_D=models.CharField(max_length=200)  
    Answer=models.CharField(choices=ANS,max_length=1,null=True)
    explanation=models.TextField(default='')
    def __str__(self):
        return self.text
class Report(models.Model):
    username=models.CharField(max_length=200,default='')
    quiz_name = models.CharField(max_length=250)
    passing_percentage=models.IntegerField(default=0)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,default='NA')
    def __str__(self):
        return self.username


