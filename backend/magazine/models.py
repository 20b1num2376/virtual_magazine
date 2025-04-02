# myapp/models.py

from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    TYPES = (
        (1, 'General knowledge'),
        (2, 'IT knowledge'),
    )
    
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPES)
    created_date = models.DateField()
    source = models.CharField(max_length=255, null=True, blank=True)
    image1 = models.FileField(upload_to='news_images/', null=True, blank=True)
    image2 = models.FileField(upload_to='news_images/', null=True, blank=True)
    image3 = models.FileField(upload_to='news_images/', null=True, blank=True)
    image4 = models.FileField(upload_to='news_images/', null=True, blank=True)

    def __str__(self):
        return self.title
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
class test(models.Model):
    test=models.OneToOneField(User, on_delete=models.CASCADE)



class Quiz(models.Model):
    title = models.CharField(max_length=255)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


    def __str__(self):
        return self.text
class Discussion(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='discussion_images/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title