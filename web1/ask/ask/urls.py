from django.conf.urls import patterns, include, url
from django.contrib import admin
from qa.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
    url(r'^$', paginator_page),
    url(r'^base/.*$', main_page),
    url(r'^login/.*$', login),
    url(r'^logout/.*$', logout_view),
    url(r'^signup/.*$', signup),
    url(r'^ask/.*$', ask),
    url(r'^signup/.*$', main_page),
    url(r'^popular/.*$', paginator_popular),
    url(r'^new/.*$', main_page),
    url(r'^question/(?P<id>\d+)/.*$', question_page),
    url(r'^answer/(?P<id>\d+)/.*$', answer_page),
    url(r'^questionansw/$', question_answ),
    url(r'^mysql/$', mysql_pull),
    url(r'^add_mysql/$', add_mysql_pull),
    url(r'^blog/main/.*$', blog_page),
    url(r'^blog/question/.*$', blog_que),

)
