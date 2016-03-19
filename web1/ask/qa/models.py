# ~*~ coding: utf-8 ~*~
from django.db import models
import datetime as dt
from django.core.paginator import Paginator
from django.contrib.auth.models import User
# Create your models here.
class MyUser(models.Model):
    first_name = models.CharField(max_length=20, blank=False, default='user')
    last_name = models.CharField(max_length=30, blank=False, default='user')
    email = models.EmailField(blank=False, default='user@user.com')
    username = models.CharField(max_length=100, blank=False, default='user123')
    password = models.CharField(max_length=20, blank=False, default='user')
    def __unicode__(self):
        return self.last_name + ' ' + self.first_name + ' ' + '(' + self.email + ')'

class UserUU(models.Model):
    username = models.CharField(unique=True,max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    def __unicode__(self):
        return self.username + "(" + self.password + ")"

### Question - вопрос
#title - заголовок вопроса
#text - полный текст вопроса
#added_at - дата добавления вопроса
#rating - рейтинг вопроса (число)
#author - автор вопроса
#likes - список пользователей, поставивших "лайк"
##
count = 0
class Question(models.Model):
    title = models.CharField(max_length=50, blank=False, default='NAN')
    text = models.CharField(max_length=200, blank=False, default='NAN')
    added_at = models.DateTimeField(blank=True, default=dt.datetime.now())
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title
    def get_url(self):
        return "/question/%s/" % self.pk
    def get_pk(self):
        return


###Answer - ответ
#text - текст ответа
#added_at - дата добавления ответа
#question - вопрос, к которому относится ответ
#author - автор ответа
###
class Answer(models.Model):
    text = models.CharField(max_length=200, blank=False, default='NAN')
    added_at = models.DateTimeField(blank=True, default=dt.datetime.now())
    question = models.ForeignKey(Question,null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return self.text
    def get_url(self):
        return "/answer/%s/" % self.pk
class SessionSS(models.Model):
    key = models.CharField(unique=True, max_length=50)
    user = models.ForeignKey(User)
    expires = models.DateTimeField()
    def __unicode__(self):
        return "session " + self.key

def paginator(request, qs, order):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    questions = qs.order_by(order)
    paginator = Paginator(questions, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

#def do_login(login, password):
#    try:
#        user = User.objects.get(username=login)
#    except User.DoesNotExist:
#        return None
#    if user.password != password:
#        return None
#    session = Session()
#    session.key = user.pk
#    session.user = user
##    session.expires = dt.datetime.now() + dt.timedelta(days=5)
#   session.save()
#    return session.key

#def session_p(request):
#    try:
#        sessid = request.COOKIES.get('sessid')
#        print ('ID=' + sessid)
#        session = Session.objects.get(key=sessid)
#        print (session)
#        request.session = session
#        request.user = session.user
#        print (request.session)
#    except Session.DoesNotExist:
#        request.session = None
#        request.user = None


