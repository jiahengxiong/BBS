#!/usr/bin/python

print('Content-type: text/html\n')

import sys, cgi, psycopg2


form = cgi.FieldStorage()
id = form.getvalue('id')  # 获取URL中的id参数
try:
    id = int(id)  # 将id转换为整数类型
except:  # 如果转换异常
    print('无效的消息id！')
    sys.exit()  # 退出脚本执行


print('''
<!DOCTYPE html>
<html lang="zh_cn">
<head>
    <meta charset="utf-8">
</head>
<body>
''')

id = str(id)

conn = psycopg2.connect(database='baz', user='postgres', password='123456')
curs = conn.cursor()
sql = "delete from messages where id=%s or reply_to=%s" %(id,id)
curs.execute(sql)
conn.commit()
print('''
<font size="2" color="green">删除成功</font>
<hr/>
<a href="main.py"><font size="2">返回首页</font></a>
 ''')

print('''
</body>
</html>
''')

