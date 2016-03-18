from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from models import *
import datetime as dt
from django.contrib.auth.models import User
from forms import *
from django.contrib.auth import authenticate, logout
from django.contrib import auth



# Create your views here.
def main_page(request):
    return HttpResponse(status=200)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
           # username = form.cleaned_data['username']
            #password = form.cleaned_data['password']
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)

            user = authenticate(username=username, password=password)
            print (user is not None)
            if user is not None:
                if user.is_active:
                    print(request.user)
                    auth.login(request, user)
                    return HttpResponseRedirect('/question/2/')
                else:
                    logout(request)
            else:
                return HttpResponseRedirect('/')
    form = LoginForm()
    return render(request, 'stack/html/pages/login_form.html',
                  {
                      'form': form
                  }
                  )
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user123 = form.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            auth.login(request, user)
            #sessid = do_login(login, password)
            #response.set_cookie('sessid', sessid, httponly=True, expires = dt.datetime.now() + dt.timedelta(days=5))
            return HttpResponseRedirect('/')
        else:
            form = SignupForm()
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'stack/html/pages/signup_form.html',
                  {
                      'form': form
                  }
                  )


def mysignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login = form.cleaned_data['username']
            password = form.cleaned_data['password']
            response = HttpResponseRedirect('/')
            #sessid = do_login(login, password)
            #response.set_cookie('sessid', sessid, httponly=True, expires = dt.datetime.now() + dt.timedelta(days=5))
            return response
    else:
        form = SignupForm()
    return render(request, 'stack/html/pages/signup_form.html',
                  {
                      'form': form
                  }
                  )
def mylogout(request):
    sessid = request.COOKIE.get('sessid')
    if sessid is not None:
        #Session.objects.delete(key=sessid)
        url = request.GET.get('continue', '/')
        return HttpResponseRedirect(url)
def mylogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print (form)
        login = form.cleaned_data['username']
        password = form.cleaned_data['password']
        #sessid = do_login(login, password)
        #if sessid:
        ##    response = HttpResponseRedirect('/')
        #    response.set_cookie('sessid', sessid, httponly=True, expires = dt.datetime.now() + dt.timedelta(days=5))
        #    return response
    else:
        form = LoginForm()
    return render(request, "stack/html/pages/login_form.html", {'form' : form})



def answer_page(request,id):
    try:
        id_safe = int(id)
    except ValueError:
        raise Http404
    try:
        answer = Answer.objects.get(pk=id_safe)
    except Answer.DoesNotExist:
        raise Http404
    return render(request, 'stack/html/pages/answer.html',
              {
                  'post' : answer
              }
              )

def question_page(request, id):
    user = request.user
    print(user)
    try:
        id_safe = int(id)
    except ValueError:
        raise Http404
    try:
        question = Question.objects.get(pk=id_safe)
    except Question.DoesNotExist:
        raise Http404
    form = AnswerForm(initial={'question': id_safe})
    answers = Answer.objects.filter(question=question)
    answers = answers[:]
    return render(request, 'stack/html/pages/question.html',
                  {
                      'post' : question,
                      'form' : form,
                      'answers' : answers
                  }
                  )

def question_answ(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        print (form.is_valid())
        if form.is_valid():
            question = Question.objects.get(id=form.cleaned_data['question'])
            text = form.cleaned_data['text']
            answer = form.save(question, text)
            url = answer.get_url()
            return HttpResponseRedirect(url)
    return HttpResponseRedirect('/')

def paginator_page(request):
    questions = Question.objects.all()
    page = paginator(request, questions, '-id')
    page.paginator.baseurl = '/?page='
    return render(request, 'stack/html/pages/paginator.html',
                  {
                      'posts' : page.object_list,
                      'paginator' : page.paginator,
                      'page' : page
                  }
                  )
def paginator_popular(request):
    questions = Question.objects.all()
    page = paginator(request, questions, '-rating')
    page.paginator.baseurl = '/popular/?page='
    return render(request, 'stack/html/pages/paginator.html',
                  {
                      'posts' : page.object_list,
                      'paginator' : page.paginator,
                      'page' : page
                  }
                  )
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'stack/html/pages/ask_form.html',
                      {
                       'form': form
                      }
                      )

def add_mysql_pull(request):
        user = User.objects.get(username='Admin',first_name='Erih',last_name='Johns',email='erih.johns@gmail.com',password='erlang')
        q = Question.objects.create(title='Difference btw Python versions', rating=55, author=user)
        return HttpResponse("added",status=200)

def mysql_pull(request):
#    user = User.objects.create(username='Admin',first_name='Erih',last_name='Johns',email='erih.johns@gmail.com',password='erlang')
    user = User.objects.create(username='Admin',email='erih.johns@gmail.com',password='erlang')

    q = Question.objects.create(title='Difference btw Python versions', rating=55, author=user, added_at='1995-3-3')
    a = Answer.objects.create(text='no comments, only emotions', question=q, author=user, added_at='1996-9-15')
    q1 = Question.objects.create(title='Difference btw Python versions2', rating=56, author=user, added_at='1999-7-30')
    a1 = Answer.objects.create(text='no comments, only emotions', question=q1, author=user, added_at='2004-10-3')
    q2 = Question.objects.create(title='Difference btw Python versions3',rating=10, author=user, added_at='1990-2-20')
    a2 = Answer.objects.create(text='no comments, only emotions', question=q2, author=user, added_at='1998-1-30')
    q3 = Question.objects.create(title='Difference btw Python versions4', rating=57, author=user, added_at='2007-1-24')
    a3 = Answer.objects.create(text='no comments, only emotions', question=q3, author=user, added_at='2002-4-12')
    q4 = Question.objects.create(title='Difference btw Python versions5', rating=59, author=user, added_at='1987-11-30')
    a4 = Answer.objects.create(text='no comments, only emotions', question=q4, author=user)
    q5 = Question.objects.create(title='Difference btw Python versions6', rating=52, author=user, added_at='2013-1-19')
    a5 = Answer.objects.create(text='no comments, only emotions', question=q5, author=user, added_at='2002-11-30')
    q6 = Question.objects.create(title='Difference btw Python versions7', rating=25, author=user, added_at='2008-12-30')
    a6 = Answer.objects.create(text='no comments, only emotions', question=q6, author=user, added_at='2005-11-30')
    q7 = Question.objects.create(title='Difference btw Python versions8', rating=35, author=user, added_at='1999-7-30')
    a7 = Answer.objects.create(text='no comments, only emotions', question=q7, author=user, added_at='2000-1-30')
    q8 = Question.objects.create(title='Difference btw Python versions9',rating=18, author=user, added_at='1999-11-14')
    a8 = Answer.objects.create(text='no comments, only emotions', question=q8, author=user, added_at='2002-12-15')
    q9 = Question.objects.create(title='Difference btw Python versions10', rating=45, author=user, added_at='1999-1-16')
    a9 = Answer.objects.create(text='no comments, only emotions', question=q9, author=user, added_at='2010-11-30')
    q10 = Question.objects.create(title='Difference btw Python versions11', rating=12, author=user, added_at='1997-6-30')
    a10 = Answer.objects.create(text='no comments, only emotions', question=q10, author=user, added_at='1998-11-30')
    q11 = Question.objects.create(title='Difference btw Python versions12', rating=51, author=user, added_at='1980-1-24')
    a11 = Answer.objects.create(text='no comments, only emotions', question=q11, author=user, added_at='1990-11-30')
    q12 = Question.objects.create(title='Difference btw Python versions13', rating=95, author=user, added_at='1981-11-30')
    a12 = Answer.objects.create(text='no comments, only emotions', question=q12, author=user, added_at='1990-5-30')
    q13 = Question.objects.create(title='Difference btw Python versions14', rating=50, author=user, added_at='2002-12-30')
    a13 = Answer.objects.create(text='no comments, only emotions', question=q13, author=user, added_at='2002-1-13')
    q14 = Question.objects.create(title='Difference btw Python versions15', rating=52, author=user, added_at='2002-11-10')
    a14 = Answer.objects.create(text='no comments, only emotions', question=q14, author=user, added_at='2003-11-30')
    q15 = Question.objects.create(title='Difference btw Python versions16', rating=1, author=user, added_at='2002-11-30')
    a15 = Answer.objects.create(text='no comments, only emotions', question=q15, author=user, added_at='2002-12-30')
    q16 = Question.objects.create(title='Difference btw Python versions17', rating=5, author=user, added_at='2005-11-30')
    a16 = Answer.objects.create(text='no comments, only emotions', question=q16, author=user, added_at='2013-11-3')
    q17 = Question.objects.create(title='Difference btw Python versions18', rating=512, author=user, added_at='2000-12-18')
    a17 = Answer.objects.create(text='no comments, only emotions', question=q17, author=user, added_at='1997-11-30')
    q18 = Question.objects.create(title='Difference btw Python versions19', rating=58, author=user, added_at='1999-11-30')
    a18 = Answer.objects.create(text='no comments, only emotions', question=q18, author=user, added_at='2001-4-3')
    q19 = Question.objects.create(title='Difference btw Python versions20', rating=335, author=user, added_at='1981-11-30')
    a19 = Answer.objects.create(text='no comments, only emotions', question=q19, author=user, added_at='1995-11-30')
    q20 = Question.objects.create(title='Difference btw Python versions21', author=user, added_at='2000-11-30')
    a20 = Answer.objects.create(text='no comments, only emotions', question=q20, author=user, added_at='2012-10-30')
    return HttpResponse('Ok',status=200)