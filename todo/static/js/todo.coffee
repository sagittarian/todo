logged_in = no
csrftoken = null
default_priority = 'medium'
priorities = ["low", "medium", "high"]

$(document).ajaxSend (event, jqxhr, settings) ->
  if settings.url.slice(0, 1) is "/" and settings.type is 'POST'
    jqxhr.setRequestHeader 'X-CSRFToken', csrftoken

$(document).ajaxSuccess (event, xhr, settings) ->
  data = $.parseJSON xhr.responseText
  csrftoken = data.csrftoken if data.csrftoken?

$.extend $.facebox.settings, 
  loadingImage : 'img/loading.gif',
  closeImage   : 'img/closelabel.png',

display_messages = (data) ->
  $msgs = $('#messages').empty()
  if data.error?
    $msgs.appendEl '.error', text: data.error
  if data.status?
    $msgs.appendEl '.info', text: data.status

get_header_row = ->
  $.el('tr.table-header').appendEl('th')
    .appendEl('th', text: 'Item').appendEl('th', text: 'Priority')

get_priority_widget = (current=default_priority) ->
  result = $.el 'select'
  for priority in priorities
    opt = $.el 'option', value: priority, text: priority
    if priority is current
      opt.attr 'selected', true
    result.append opt
  result.change ->
    $el = $(this)
    value = $el.find('option:selected').val()
    {id, old_priority} = $el.parent().data()
    url = '/api/todo/modify/'
    data = id: id, priority: value
    $.post url, data, (data, success, xhr) ->
      if data.error?
        $el.text old_priority
      else
        $el.parent().data 'old_priority', value
      display_messages data
  return result

get_delbtn = ($parent) ->
  result = $parent.el 'td.delbtn', 
    html: '<a href="" class="delete-btn">X</a>'
  result.click del_item
  return result

get_login_info = ->
  url = '/api/account/'
  $.get url, (data, textStatus, jqXHR) ->
    return if data.error?
    set_login_info data.username
    if data.username?
      setlist()
    
set_login_info = (username) ->
  $header = $('#account-info').empty()
  if username?
    $logout = $.el 'a.logout', href: '', text: 'Log out'
    $changepw = $.el 'a.change-password', 
      href: '#password-change', text: 'change password'
    $header.el('span', text: "Welcome, #{username}! ")
      .append($logout).appendEl('span', text: ' or ').append($changepw)
    $logout.click ajax_logout
    $changepw.facebox()
  else
    $loginlink = $.el 'a.login', href: "#login", text: 'Log in'
    $registerlink = $.el 'a.register', href: "#register", text: 'Sign up'
    $header.el('span').append($loginlink).appendEl('span', text: ' or ')
      .append($registerlink)
    $loginlink.facebox()
    $registerlink.facebox()

ajax_logout = ->
  url = '/api/account/logout/'
  $.get url, account_callback
  return no

del_item = (e) ->
  $row = $(this).parent()
  id = $row.data 'id'
  url = '/api/todo/delete/'
  data = id: id
  $.post url, data, (result, success, xhr) ->
    $row.remove() unless result.error?
    display_messages result
  return no

edit_cell = (value, settings) ->
  $el = $(this)
  {id, old_label} = $(this).parent().data()
  url = '/api/todo/modify/'
  data = id: id, label: value
  $.post url, data, (data, success, xhr) ->
    if data.error?
      $el.text old_label
    else
      $el.parent().data 'old_label', value
    display_messages data
  return value
  
add_cell = (value, settings) ->
  url = '/api/todo/add/'
  data = label: value
  $.post url, data, (result, success, xhr) ->
    display_messages result
    $parent = settings.itemtd.parent()
    if result.error?
      $parent.remove()
      return
    $parent.data 
      id: result.id, old_label: value, old_priority: default_priority
    $parent.removeClass().addClass 'todoitem'
    settings.itemtd.editable 'destroy'
    settings.itemtd.editable edit_cell
    settings.prioritytd.editable edit_priority,
      type: 'select'
      data: priorities
  return value

setlist = ->
  url = '/api/todo/getlist/'
  $.get url, (data, textStatus, jqXHR) ->
    display_messages data
    return if data.error?
    $('.additem-btn').show()
    $tdlist = $('.todolist').empty().append get_header_row()
    for item in data.items
      $tr = $tdlist.el 'tr.todoitem'
      $delbtn = get_delbtn $tr
      $item = $tr.el 'td.item', text: item.label
      $tr.append get_priority_widget(item.priority)
      $tr.data 
        old_label: item.label, old_priority: item.priority, id: item.id
      $item.editable edit_cell

additem = ->
  $tdlist = $('.todolist')
  $newrow = $tdlist.el 'tr.newitem'
  $delbtn = get_delbtn $newrow
  $item = $newrow.el 'td.item'
  $priority = get_priority_widget().appendTo $newrow 
  $item.editable add_cell, 
    onblur_cb: -> $newrow.remove()
    row: $newrow
    itemtd: $item
    prioritytd: $priority 
  $item.click()
  return no

# Callback for AJAX requests that do account related things. 
account_callback = (data, success, xhr) ->
  display_messages data
  if not data.error?
    set_login_info data.username
    if not data.username?
      $('.todolist').empty()
      $('.additem-btn').hide()
  $(document).trigger 'close.facebox'

$ ->
  get_login_info()
  $('.additem-btn').click additem
  $('.facebox').facebox()
  $(document).on 'reveal.facebox', (revealevent) ->
    $('a.facebox').facebox()
    $('form').on 'submit', (e) ->
      e.preventDefault()
      $form = $(this)
      url = $form.attr 'action'
      data = $form.serialize()
      $.post url, data, (data, success, xhr) ->
        account_callback data, success, xhr
        if $form.data('refresh') is 1
          setlist()
