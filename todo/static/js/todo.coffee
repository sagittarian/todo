logged_in = no
csrftoken = null
default_priority = 1

$(document).ajaxSend (event, jqxhr, settings) ->
  if settings.url.slice(0, 1) is "/" and settings.type is 'POST'
    jqxhr.setRequestHeader 'X-CSRFToken', csrftoken

get_header_row = ->
  $.el('tr.header').appendEl('th')
    .appendEl('th', text: 'Item').appendEl('th', text: 'Priority')

get_delbtn = ($parent) ->
  result = $parent.el 'td.delbtn', 
    html: '<a href="" class="delete-btn">X</a>'
  result.click del_item
  return result

get_login_info = ->
  url = '/api/account/'
  $.get url, (data, textStatus, jqXHR) ->
    csrftoken = data.csrftoken
    return if data.error?
    set_login_info data.username
    
set_login_info = (username, msg='') ->
  $header = $('.header').empty()
  if username?
    $header.el 'div', 
      html: "Welcome #{username}! #{msg} <a href=''>Sign out</a>"
  else
    $header.el('div')
      .appendEl('a.login', href: "", text: 'Log in')
      .appendEl('span', text: ' or ')
      .appendEl('a.signup', href: "", text: 'Sign up')

del_item = (e) ->
  $row = $(this).parent()
  id = $row.data 'id'
  url = '/api/todo/delete/'
  data = id: id
  $.post url, data, (result, succes, xhr) ->
    $row.remove()
  return no

edit_cell = (value, settings) ->
  id = $(this).parent().data 'id'
  url = '/api/todo/modify/'
  data = id: id, label: value
  $.post url, data
  return value
  
edit_priority = (value, settings) ->
  id = $(this).parent().data 'id'
  url = '/api/todo/modify/'
  data = id: id, priority: value
  $.post url, data
  return value

add_cell = (value, settings) ->
  url = '/api/todo/add/'
  data = label: value
  $.post url, data, (result, success, xhr) ->
    $parent = settings.itemtd.parent()
    $parent.data 'id', result.id
    $parent.removeClass().addClass 'todoitem'
    settings.itemtd.uneditable()
    settings.itemtd.editable edit_cell
    settings.prioritytd.editable edit_priority
  return value

setlist = ->
  url = '/api/todo/getlist/'
  $.get url, (data, textStatus, jqXHR) ->
    csrftoken = data.csrftoken
    return if data.error?
    $tdlist = $('.todolist').empty().append get_header_row()
    for item in data.items
      $tr = $tdlist.el 'tr.todoitem'
      $delbtn = get_delbtn $tr
      $item = $tr.el 'td.item', text: item.label
      $priority = $tr.el 'td.priority', text: item.priority
      $tr.data 'id', item.id
      $item.editable edit_cell
      $priority.editable edit_priority

additem = ->
  $tdlist = $('.todolist')
  $newrow = $tdlist.el 'tr.newitem'
  $delbtn = get_delbtn $newrow
  $item = $newrow.el 'td.item'
  $priority = $newrow.el 'td.priority', text: default_priority
  $item.editable add_cell, 
    onblur_cb: -> $newrow.remove()
    row: $newrow
    itemtd: $item
    prioritytd: $priority 
  $item.click()
  return no

$ ->
  get_login_info()
  setlist()
  $('.additem-btn').click additem
