import os
import sqlite3
from sys import platform

conn=''
def getdb():
	global conn
	if platform=='linux':
		path='~/.mozilla/firefox'
		dr=os.popen('ls -d '+path+'/*/').read().split()
		#print(dr)
		for i in dr:
			if 'default' in i:
				path=i+'cookies.sqlite'
				break
		os.system('cp '+path+' /tmp/')
		path='/tmp/cookies.sqlite'
		conn=sqlite3.connect(path)
		return conn

def getauth():
	cur=conn.cursor()
	al=cur.execute("SELECT * FROM moz_cookies where baseDomain LIKE '%coursera%' AND name='CAUTH'")
	for i in al:
		return i[4]