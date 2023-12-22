from django.db import models
from django.contrib.auth.models import User
import random
from django.db import models
from PIL import Image


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    number_of_questions = models.IntegerField(default=1)
    time = models.IntegerField(help_text="Duration of the quiz in seconds", default="1")

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all()


class Question(models.Model):
    qn = models.CharField(max_length=200)
    marks = models.IntegerField(default=5)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.qn

    def get_answers(self):
        return self.answer_set.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='avatar.jpg',  # default avatar
        upload_to='profile_avatars'  # dir to store the image
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"question: {self.question.qn}, answer: {self.choices}, correct: {self.correct}"


class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)