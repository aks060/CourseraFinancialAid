#!/usr/bin/python3
import requests
import threading
import os
import json
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
			if '.Parrot' in i:
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

conn=getdb()
s=requests.session()
req=''
sess=getauth()
if sess is None:
	sess=input('Enter your CAUTH ID: ')
def getres(url, type='g'):
	global s, req
	if type=='g':
		req=s.get(url)
	elif type=='p':
		req=s.post(url)
s.cookies['CAUTH']=sess;
url=input('Enter your URL of course page: ')
typ=input('Enter the Course Type (Cyber Security, ML)')
t=threading.Thread(target=getres, args=(url, ))
t.start()
t.join()
req=req.content.decode()
ind=req.find('courseId')
req1=req[ind:(ind+8000)]
req1=req1.split('"')
courseid=req1[2]
print('courseidind: '+courseid)

ind=req.find('userData')
req1=req[ind:(ind+8000)]
req1=req1.split('"')
userid=req1[3][1:-1]
print('userid: '+userid)

#userid=req1[req1.index('userData')+3][1:-1]
#courseid=req1[courseidind+2]
head={
	'Host': 'www.coursera.org',
	'Content-Type': 'application/json; charset=utf-8',
	'Content-Length': '227'
}
req=s.post('https://coursera.org/api/carts.v2', json={"userId":int(userid),"currencyCode":"INR","countryIsoCode":"IN","auxiliaryCartInfo":[], "productItems":[{"productType":"VerifiedCertificate","productItemId":courseid,"productAction":"Buy","cartItemIdToRefund":{}}]}, headers=head)
dat=req.json()
cartid=dat['elements'][0]['id']
req=s.post('https://coursera.org/api/financialAidApplications.v2', json={"whyApplying":"I live only for my scholarship. It's really impossible for me to pay for this course. Financial Aid will help me take this course without any adverse impact on my monthly essential needs. I want to take this course as I want to complete the "+typ+" Specialization on Coursera. I want to complete the "+typ+" Specialization. This Specialization will boost my job prospects after graduation from my institute. It will help perform better in carrying out "+typ+" and give me an edge over my competitors. A verified certificate will attach credibility to the certificate I receive from this course. I plan to complete all assignments on or before time as I have done in previous Signature Track Courses. Also I intend to participate in Discussion Forums, which I have found to supplement my learning immensely in the other online courses I have taken on Coursera. I also plan to grade assignments which are to peer reviewed which I believe will an invaluable learning opportunity.","annualIncome":"0","cartId":int(cartid),"educationalBackground":"Some college","employmentStatus":"Student","affordToPay":0,"payPeriod":"per month","howContributeToCareer":"I’m a student from India and want to learn "+typ+". I think it will be beneficial for my thesis work. But I’ve no job of my own to carry the expanses to pay for the certificate of this course. I live only for my scholarship. In this circumstance, it is very much difficult for me to gather such amount of money for the certificate. Financial Aid will help me take this course without any adverse impact on my monthly essential needs. So I’m badly in need of this financial aid. I want to take this course as I want to learn "+typ+". I plan to complete all assignments on or before time as I have done in previous Signature Track Courses. Also I intend to participate in Discussion Forums, which I have found to supplement my learning immensely in the other online courses I have taken on Coursera. I also plan to grade assignments which are to peer reviewed which I believe will an invaluable learning opportunity.","willingToTakeOutLoan":False,"whyNotWillingToTakeLoan":"I want to complete the "+typ+". This Course will boost my job prospects after graduation from my institute. It will help perform better in carrying out "+typ+" and give me an edge over my competitors. A verified certificate will attach credibility to the certificate I receive from this course. It's really impossible for me to pay for this course. Financial Aid will help me take this course without any adverse impact on my monthly essential needs. I want to take this course as I want to complete the "+typ+" Specialization on Coursera. I plan to complete all assignments on or before time as I have done in previous Signature Track Courses. Also I intend to participate in Discussion Forums, which I have found to supplement my learning immensely in the other online courses I have taken on Coursera. I also plan to grade assignments which are to peer reviewed which I believe will an invaluable learning opportunity."}, headers=head)
try:
	dat=req.json()
	print('You have already applied for the Financial Aid for this Course')
except Exception as e:
	print('Financial Aid Applied Successfully')
