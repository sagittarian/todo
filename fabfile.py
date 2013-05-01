from fabric.api import *
import os.path

env.user = 'mesha'
env.hosts = ['mesha.webfactional.com']

BASEDIR = '/home/amesha/projects/todo'

def coffee():
    with lcd(BASEDIR):
        with lcd('todo/static/js'):
            local('coffee -c todo.coffee')
        local('echo yes | ./manage.py collectstatic')

def watch_cs():
    with lcd(os.path.join(BASEDIR, 'todo/static/js')):
        local('coffee -cw todo.coffee')

def buildjs():
    coffee()
    with lcd(BASEDIR):
        files = ['jquery-el/jquery-el.js',
                 'jquery_jeditable/jquery.jeditable.js',
                 'facebox/src/facebox.js',
                 'todo/static/js/todo.js']
        local('cat {} > todo/static/js/todo.all.js'.format(' '.join(files)))
        with lcd('todo/static/js'):
            local('yui-compressor todo.all.js -o todo.min.js')
