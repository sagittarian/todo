from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from annoying.functions import get_object_or_None

from todo.decorators import *

from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')


class AjaxRequireFieldFactory(object):
    '''Factory to create decorators that will require the given field
    in the POST data and pass in on to the underlying function as a
    keyword argument.

    If required is True, then if the field is missing or empty an
    ajax error will be returned. If it is False, then the underlying function
    will simply be passed None.'''

    def __init__(self, field, required=True):
        self.field = field
        self.required = required

    def __call__(self, func):
        def newfunc(request, *args, **kw):
            if self.field in request.POST:
                kw[self.field] = request.POST[self.field]
            elif self.required:
                return {'error': '{} is required'.format(self.field)}
            else:
                kw[self.field] = None
            return func(request, *args, **kw)
        return newfunc

ajax_require_username = AjaxRequireFieldFactory('username', required=True)
ajax_require_password = AjaxRequireFieldFactory('password', required=True)
ajax_get_email = AjaxRequireFieldFactory('email', required=False)


#************* Views ***************

@ajax_request
def info(request):
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = None
    return {'username': username}


@ajax_request
@ajax_requires_POST
@ajax_require_username
@ajax_get_email
@ajax_require_password
def login_view(request, username, email, password, create_user=True):
    if create_user:
        try:
            User.objects.create_user(username, email, password)
        except IntegrityError:
            return {'error': 'Username is already taken'}
    new_user = authenticate(username=username, password=password)
    if new_user is not None:
        login(request, new_user)
        return {'username': new_user.username}
    else:
        return {'username': None, 'error': 'Invalid username or password'}


@ajax_request
def logout_view(request):
    logout(request)
    return {'username': None, 'status': 'You have been logged out'}


@ajax_request
@ajax_requires_login
@ajax_requires_POST
@ajax_require_password
def password_change(request, password):
    request.user.set_password(password)
    request.user.save()
    return {'username': request.user.username,
            'status': 'Your password has been changed'}


@ajax_request
@ajax_requires_POST
@ajax_require_username
def password_reset(request, username):
    user = get_object_or_None(User, username=username)
    if user is not None:
        newpw = User.objects.make_random_password()
        user.set_password(newpw)
        user.save()

        context = {'username': user.username, 'password': newpw}
        subject = render_to_string('ajaxreg/reset_email_subject.txt', context)
        subject = ' '.join(subject.split())  # No newlines
        message = render_to_string('ajaxreg/reset_email_body.txt', context)
        send_mail(subject, message, from_addr, [user.email],
                  fail_silently=True)

    return {'status': 'A new password has been emailed to you'}
