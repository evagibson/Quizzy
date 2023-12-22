from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Quiz, Question, Answer, Marks_Of_User
from app.forms import QuizForm, QuestionForm, UserUpdateForm, ProfileUpdateForm
from django.forms.models import inlineformset_factory
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def events(request):
    return render(request, 'events.html')


def contact(request):
    return render(request, 'contact.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect(signup)
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                password=password, email=email)
                user.set_password(password)
                user.save()
                return redirect('login')
    else:
        print("this is not post method")
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def base(request):
    return render(request, 'base.html')


def create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("/quizzes")
    else:
        form = QuizForm()
        return render(request, 'create.html', {'form': form})


def quizzes(request):
    quizs = Quiz.objects.all()
    return render(request, 'quizzes.html', {'quizs': quizs})


def delete(request, id):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()
    return redirect('/quizzes')


def add_question(request, quiz_id):
    QuestionFormSet = inlineformset_factory(Quiz, Question, fields=('qn', 'marks'), extra=4)
    quiz = Quiz.objects.get(pk=quiz_id)
    formset = QuestionFormSet(queryset=Question.objects.none(), instance=quiz)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST, instance=quiz)
        if formset.is_valid():
            formset.save()
            return redirect("question", quiz_id=quiz.id)
    else:
        formset = QuestionFormSet(instance=quiz)
    return render(request, "add_question.html", {'formset': formset})


def add_options(request, myid):
    OptionsFormSet = inlineformset_factory(Question, Answer, fields=['choices', 'correct', 'question'], extra=4)
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        formset = OptionsFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return redirect("add_options", myid=question.id)
    else:
        formset = OptionsFormSet(instance=question)
    return render(request, "add_options.html", {'formset': formset, 'question':question})


def question(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'questions.html', {'questions': questions, 'quiz_id': quiz_id})


def edit(request, id):
    quiz = Quiz.objects.get(id=id)
    return render(request, 'edit.html', {'quiz', quiz})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz.html", {'quiz': quiz})


def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.choices)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, myid):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.filter(qn=k).first()
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.qn)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.choices:
                        if a.correct:
                            score += 1
                            correct_answer = a.choices
                    else:
                        if a.correct:
                            correct_answer = a.choices

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})

        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)

        return JsonResponse({'passed': True, 'score': score, 'marks': marks})


def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "results.html", {'marks':marks})


def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/results')
    return render(request, "delete_result.html", {'marks':marks})


def search_quizzes(request):
    if request.method == "POST":
        searched = request.POST['searched']
        quizzes = Quiz.objects.filter(title__contains=searched)

        return render(request, "search_quizzes.html",{'searched':searched, 'quizzes':quizzes})
    else:
        return render(request, "search_quizzes.html",{})