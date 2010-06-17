import e32
import contacts
import appuifw
import key_codes
import urllib

def py_fetion_quit():
    exit = appuifw.query(u'Do you really want to exit?', "query")
    if exit:
        app_lock.signal()

def py_fetion_send(username, password, sendto, message):
    fetion = {'username':username,\
    'password':password,\
    'sendto':sendto,\
    'message':message.encode('utf-8')}
    request = urllib.urlencode(fetion)
    service = 'http://sms.api.bz/fetion.php?'
    f = urllib.urlopen(service+request)
    return f.read()

def py_fetion_message(id = -1):
    message = None
    sendto =  None
    if id == -1:
        key = lb.current()
    else:
        key = id
    sendto = lb_list[key][1]
    message = appuifw.query(u"Type the Message", "text", u"PyFetion")
    if message and sendto:
        note = u"Sending to " + lb_list[key][0]
        appuifw.note(note, "info")
        sent = py_fetion_send(NAME, PASSWORD, sendto, message)

def about():
    appuifw.note(u"PyFetion!")

def search():
    search_list = []
    for i in lb_list:
        search_list.append(i[0])
    search_id = None
    search_id = appuifw.selection_list(search_list, 1)
    if search_id:
        py_fetion_message(search_id)


NAME = u'136718547232'
PASSWORD = u'tsyj139wereer'
appuifw.note(u"Waiting ...", "info")

# open the contacts database
c = contacts.open()
# get the contacts
lb_list = []
lb_temp = {}
for i in c.keys():
    for j in c[i]:
       lb_temp[j.type] = j.value
    lb_list.append((c[i].title, lb_temp[u'mobile_number']))
    lb_temp = {}
c = None

# create a listbox
lb = appuifw.Listbox(lb_list)
# bind the callback func. for SelectKey
lb.bind(key_codes.EKeySelect, py_fetion_message)
lb.bind(key_codes.EKeyStar, search)
# set the app body
appuifw.app.body = lb
appuifw.app.screen = "normal"

menu_item = [(u"Search",search),(u"About",about)]
appuifw.app.menu = menu_item

appuifw.app.exit_key_handler = py_fetion_quit
appuifw.app.title = u"PyFetion"

app_lock = e32.Ao_lock()
app_lock.wait()