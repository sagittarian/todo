#********** Some useful utility decorators ***********
from django.core.context_processors import csrf

from annoying.decorators import ajax_request as _ajax_request

def ajax_request(func):
    '''Return a JSON response from the provided dict or list from the
    decorated view, and add an error: null key if it doesn't already
    have an error key.'''
    @_ajax_request
    def newfunc(request, *args, **kw):
        csrftoken = unicode(csrf(request)['csrf_token'])
        result = {'error': None, 'csrftoken': csrftoken}
        response = func(request, *args, **kw)
        if isinstance(response, dict):
            result.update(response)
        else:
            result = response
        return result
    return newfunc

def ajax_requires_login(func):
    '''Decorator to return a simple JSON object with an error message
    if the user is not authenticated.'''
    def newfunc(request, *args, **kw):
        if not request.user.is_authenticated():
            return {'error': 'Not logged in'}
        result = {'error': None}
        result.update(func(request, *args, **kw))
        return result
    return newfunc


def ajax_requires_POST(func):
    '''Decorator to return a simple JSON object with an error message
    if the request was not sent via POST'''
    def newfunc(request, *args, **kw):
        if request.method != 'POST':
            return {'error': 'Request must be sent via POST'}
        return func(request, *args, **kw)
    return newfunc
