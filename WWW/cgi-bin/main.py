#!/usr/bin/python

print('Content-type: text/html\n')

import cgitb;

cgitb.enable()

import psycopg2.extras

conn = psycopg2.connect(database='baz', user='postgres', password='123456')
curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

print('''
<!DOCTYPE html>
<html lang="zh_cn">
<head>
    <meta charset="utf-8">
    <title>我的论坛</title>
</head>
<body>
    <h3>我的BBS</h3>
''')

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


def format_show(message):  # 创建递归函数
    print('<h5><a href="author.py?id=%(id)i">%(sender)s：</a><a href="view.py?id=%(id)i">%(subject)s</a></h5>' % message)
    print('<font size="2">{}</font>'.format(message['text']))
    try:
        kids = children[message['id']]
    except KeyError:
        pass
    else:
        print('<blockquote>')
        for kid in kids:
            format_show(kid)
        print('</blockquote>')


for message in top_level:  # 遍历顶级消息列表
    format_show(message)

print('''
<hr/>
<a href="edit.py"><font size="2">发布消息</font></a>
</body>
</html>
''')
