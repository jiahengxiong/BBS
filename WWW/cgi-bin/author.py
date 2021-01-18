#!/usr/bin/python
print('Content-type: text/html\n')

import cgitb;

cgitb.enable()

import cgi,sys, psycopg2.extras

form = cgi.FieldStorage()
id = (form.getvalue('id') ) # 获取URL中的id参数
try:
    id = int(id)  # 将id转换为整数类型
except:  # 如果转换异常
    print('无效的消息id！')
    sys.exit()  # 退出脚本执行


conn = psycopg2.connect(database='baz', user='postgres', password='123456')
curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
sql = 'select sender from messages where id=%i'%id
curs.execute(sql)
sender = curs.fetchone()[0]


print('''
<!DOCTYPE html>
<html lang="zh_cn">
<head>
    <meta charset="utf-8">
    <title>%s的主页</title>
</head>
<body>
    <h3>%s发布过的主题</h3>
'''%(sender,sender))

sql = 'select * from messages'
curs.execute(sql)
messages = curs.fetchall()

top_level = []
children = {}
for message in messages:
    parrent_id = message['reply_to']
    if parrent_id is None:
        top_level.append(message)
    else:
        children.setdefault(parrent_id, []).append(message)



for message in top_level: # 遍历顶级消息列表
    if message['sender']==sender and message['reply_to'] is None:
        print('<h5><a href="view.py?id=%(id)i">%(sender)s：%(subject)s</a></h5>' % message)
        print('<font size="2">{}</font>'.format(message['text']))


print('''
<hr/>
<a href="main.py"><font size="2">返回首页</font></a>
</body>
</html>
''')

