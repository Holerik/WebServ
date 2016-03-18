# coding=utf-8
from django import forms
import models
from django.contrib.auth.models import User


###AskForm - форма добавления вопроса
#title - поле заголовка
#text - поле текста вопроса
##
class AskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    def clean_text(self):
        text = self.cleaned_data['text']
        if not is_ethic(text):
            raise forms.ValidationError(u'Message not correct', code=12)
        return text
    def clean_title(self):
        title = self.cleaned_data['title']
        if not is_ethic(title):
            raise forms.ValidationError(u'Message not correct', code=12)
        return title
    def save(self):
        question = models.Question(**self.cleaned_data)
        question.save()
        return question



###AnswerForm - форма добавления ответа
#text - поле текста ответа
#question - поле для связи с вопросом
##
class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
    def clean_text(self):
        text = self.cleaned_data['text']
        if not is_ethic(text):
            raise forms.ValidationError(u'Message not correct', code=12)
        return text
    def save(self, question, text):

        answer = models.Answer(text=text, question=question)
        answer.save()
        return answer

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],password=self.cleaned_data['password'])
        return user
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    def clean_username(self):
        text = self.cleaned_data['username']
        if not is_ethic(text):
            raise forms.ValidationError(u'Message not correct', code=12)
        return text
    def clean_password(self):
        text = self.cleaned_data['password']
        if not is_ethic(text):
            raise forms.ValidationError(u'Message not correct', code=12)
        return text



def is_ethic(text):
    return True