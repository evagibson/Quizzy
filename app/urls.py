from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create/', views.create, name='create'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('search_quizzes/', views.search_quizzes, name='search-quizzes'),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),

    path('quizzes/add_question/<quiz_id>/', views.add_question, name='add_question'),
    path('add_options/<int:myid>/', views.add_options, name='add_options'),
    path('quizzes/add_question/<quiz_id>/questions/', views.question, name='question'),

    path("<int:myid>/", views.quiz, name="quiz"),
    path('<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    path('<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
    path('results/', views.results, name='results'),
    path('delete_result/<int:myid>/', views.delete_result, name='delete_result'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
