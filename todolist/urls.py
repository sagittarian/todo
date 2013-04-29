from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^getlist/$', 'todolist.views.getlist', name='getlist'),
    url(r'^add/$', 'todolist.views.additem', name='additem'),
    url(r'^delete/$', 'todolist.views.delitem', name='delitem'),
    url(r'^modify/$', 'todolist.views.moditem', name='moditem'),
)
