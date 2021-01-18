#!/usr/bin/python

print('Content-type: text/html\n')

import sys, cgi, psycopg2

def quote(string):  # 定义处理单引号的函数
    if string:  # 如果不是空值或None值
        return string.replace("'", "''")  # 将单引号替换为两个单引号
    else:
        return string

print('''
<!DOCTYPE html>
<html lang="zh_cn">
<head>
    <meta charset="utf-8">
</head>
<body>
''')

form = cgi.FieldStorage()
subject = quote(form.getvalue('subject'))  # 获取字段值并进行单引号处理
sender = quote(form.getvalue('sender'))  # 获取字段值并进行单引号处理
reply_to = form.getvalue('reply_to')
text = quote(form.getvalue('text'))  # 获取字段值并进行单引号处理
if reply_to is not None:  # 如果有被回复消息的id
    try:
        reply_to = int(reply_to)  # 将id转换为整数类型
    except:  # 如果转换异常
        print('''
        <font size="2" color="red">无法发布该消息！</font>
        <hr/>
        <a href="main.py"><font size="2">返回首页</font></a>
        ''')
        sys.exit()  # 退出脚本执行
if not (subject and sender and text):  # 如果有任何一个字段值为空值或者None值
    print('''
    <font size="2" color="red">请输入回复内容！</font>
    <hr/>
    <a href="edit.py?reply_to=%s"><font size="2">返回编辑</font></a>
    ''' % reply_to)
else:  # 如果是符合要求的输入
    conn = psycopg2.connect(database='baz', user='postgres', password='123456')
    curs = conn.cursor()
    if reply_to is None:  # 如果是回复消息
        sql = "insert into messages(subject,sender,text) values('%s','%s','%s')" % (subject, sender, text)
    else:  # 如果是新发布消息
        sql = "insert into messages(subject,sender,reply_to,text) values('%s','%s','%i','%s')" % (
            subject, sender, reply_to, text)
    curs.execute(sql)
    conn.commit()
    print('''
    <font size="2" color="green">发布成功</font>
    <hr/>
    <a href="main.py"><font size="2">返回首页</font></a>
    ''')

    print('''
    </body>
    </html>
    ''')