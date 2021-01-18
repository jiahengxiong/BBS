#!/usr/bin/python

print('Content-type: text/html\n')

import cgitb;

cgitb.enable()

import cgi, sys, psycopg2.extras

form = cgi.FieldStorage()
id = form.getvalue('id')  # 获取URL中的id参数

conn = psycopg2.connect(database='baz', user='postgres', password='123456')
curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

print('''
<!DOCTYPE html>
<html lang="zh_cn">
<head>
    <meta charset="utf-8">
    <title>查看消息</title>
</head>
<body>
''')
try:
    id = int(id)  # 将id转换为整数类型
except:  # 如果转换异常
    print('无效的消息id！')
    sys.exit()  # 退出脚本执行

sql = 'select * from messages where id=%i' % id
curs.execute(sql)
rows = curs.fetchall()
if not rows:  # 如果没有查询结果
    print('消息不存在！')
    sys.exit()  # 退出脚本执行
row = rows[0]  # 获取查询结果中的第一个字典
print('''
<p>
<h5>%(subject)s</h5>
<font size="2"><a href="author.py?id=%(id)i">%(sender)s</a></font></br>
<pre>%(text)s</pre>
</p>
<hr/>
<a href="main.py"><font size="2">返回首页</font></a>|
<a href="edit.py?reply_to=%(id)s"><font size="2">回复消息</font></a>
<a href="delete.py?id=%(id)s"><font size="2">删除消息</font></a>
</body>
</html>
''' % row)
