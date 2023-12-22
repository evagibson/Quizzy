from django import forms
from app.models import Quiz, Question, Profile
from django.contrib.auth.models import User


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'number_of_questions', 'time']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['qn', 'marks', 'quiz']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

