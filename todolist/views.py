from models import TodoItem, LABEL_MAX_LEN, PRIORITIES_LIST
from annoying.functions import get_object_or_None

from todo.decorators import *

#******* Decorators *******

def ajax_get_item(func):
    '''Decorator to check that an id is present in the POST data,
    retrieve that todo list item for the current user, and pass
    it on to the decorated function via a keyword argument,
    and return an error if any of that is not in order.'''
    def newfunc(request, *args, **kw):
        if 'id' not in request.POST:
            return {'error': 'Missing ID'}
        try:
            id = int(request.POST['id'])
        except ValueError:
            return {'error': 'Invalid ID'}
        item = get_object_or_None(TodoItem, pk=id, user=request.user)
        if item is None:
            return {'error': 'No such item for this user'}
        kw['item'] = item
        return func(request, *args, **kw)
    return newfunc


def ajax_get_todo_fields(func):
    '''Decorator to check if there is a priority and/or label key
    in the POST data, validate the fields and pass them on to the function
    as keyword args.

    The fields can also be missing or empty, in which case the function
    will get None for that field. (But if it is present then it must be
    valid.) Labels that are too long will currently be truncated.'''
    def newfunc(request, *args, **kw):
        priority = request.POST.get('priority', '').strip()
        if priority:
            try:
                priority = int(request.POST['priority'])
            except ValueError:
                return {'error': 'Invalid priority'}
            if priority not in PRIORITIES_LIST:
                return {'error': 'Invalid priority'}
        else:
            priority = None
        label = request.POST.get('label', '').strip()[:LABEL_MAX_LEN].strip()
        if not label:
            label = None
        kw['priority'] = priority
        kw['label'] = label
        return func(request, *args, **kw)
    return newfunc


#******* Views ********

@ajax_request
@ajax_requires_login
def getlist(request):
    '''Get the todo list for the logged in user.'''
    items = TodoItem.objects.filter(user=request.user)
    return {'items': [item.as_dict() for item in items]}


@ajax_request
@ajax_get_item
@ajax_requires_POST
@ajax_requires_login
def delitem(request, item):
    '''Delete the item with the id specified in the POST request'''
    item.delete()
    return {}


@ajax_request
@ajax_get_todo_fields
@ajax_requires_POST
@ajax_requires_login
def additem(request, label, priority):
    '''Add the item specified in the POST request with the given label
    and optional priority.'''
    if label is None:
        return {'error': 'Must provide a label for a new item'}
    kw = {'label': label, 'user': request.user}
    if priority is not None:
        kw['priority'] = priority
    item = TodoItem(**kw)
    item.save()
    return {'id': item.pk}


@ajax_request
@ajax_requires_POST
@ajax_requires_login
@ajax_get_item
@ajax_get_todo_fields
def moditem(request, item, label, priority):
    '''Modify the label and/or priority of the item with the id
    specified in the POST request.'''
    if label is not None:
        item.label = label
    if priority is not None:
        item.priority = priority
    item.save()
    return {}
