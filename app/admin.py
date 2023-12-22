from django.contrib import admin
from app.models import Quiz, Question, Profile, Answer, Marks_Of_User

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Answer)
admin.site.register(Marks_Of_User)

