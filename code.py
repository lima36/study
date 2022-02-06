# -*- coding: utf-8 -*-

import unicodedata
import re
from urllib import parse

data = u'%uC120%uD0DD%uD558%uC2E0%20%uB0A0%uC9DC%uC5D0%20%uC774%uBBF8%20%uC608%uC57D%uC774%20%uC788%uC2B5%uB2C8%uB2E4."'
data2 = u"\uC120\uD0DD\uD558\uC2E0\20\uB0A0\uC9DC\uC5D0\20\uC774\uBBF8\20\uC608\uC57D\uC774\20\uC788\uC2B5\uB2C8\uB2E4."
print(data2)
data.encode('utf-8')
print(type(data))
print(data)
print(''.join(data))

def unquote_u(source):
    result = parse.unquote(source)
    if '%u' in result:
        result = result.replace('%u','\\u').decode('unicode_escape')
    return result

data3 = data.replace('%u', '\\u').encode().decode('unicode_escape')

print(data3.replace('%20', ' '))

data = data.encode('utf-8')
data = data.decode('unicode_escape')
print(data)

test = "%uC120"
print(test.encode('euc-kr'))
print(data.encode('euc-kr'))


text = u'aaa'
print(text)

a = "\uC120"
print(a)
a = a.encode('cp949')
print(a)
# a = a.decode('unicode_escape')
print ("%s" %a)


c = u'가'      # 유니코드문자열 리터럴을 적용했다.
c.encode('cp949')
print(type(c))
c         # '가'의 코드값
print(c)       # print 할 경우에는 문자열로 표현된다.

unicode_string = "\u2665\u00C4\u00C6"
print(unicode_string)

print('Omega: \u03A9')

d = "%uC120%uD0DD%uD558"
h = d.replace(r"%u", '\\u')
print(h.encode('euc-kr'))

g = "%%%%"
f = g.replace(r"%", "\\")
print(f)

test10 = '{"result" : "OK", "gomsg" : "%uC608%uC57D%uC774%20%uC644%uB8CC%20%uB418%uC5C8%uC2B5%uB2C8%uB2E4.%20%uC608%uC57D%uD558%uC2E0%20%uC0AC%uD56D%uC744%20%uD655%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694.", "gonexturl" : "./my_golfreslist.asp"}'
test11 = eval(test10)
print(test11['gomsg'].replace('%u', '\\u').encode().decode('unicode_escape').replace('%20', ' '))
print(type(eval(test10)))

test21 = '{"result" : "OK", "gomsg" : "%uC608%uC57D%uC774%20%uC644%uB8CC%20%uB418%uC5C8%uC2B5%uB2C8%uB2E4.%20%uC608%uC57D%uD558%uC2E0%20%uC0AC%uD56D%uC744%20%uD655%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694.", "gonexturl" : "./my_golfreslist.asp"}'
test22 = eval(test21)

tt=ord("정")
print("%x"%tt)
# %uC815%uD604%uAD6D
# dd=tt.encode('utf-8')
# print(parse.quote(tt))

a= [hex(ord(x)) for x in u"정현국"]
total=""
for aa in a:
    d= aa.replace('0x', '%u')
    print(d)
    total += d

print(total)

res='{"result" : "OK", "gomsg" : "%uC608%uC57D%uC774%20%uC644%uB8CC%20%uB418%uC5C8%uC2B5%uB2C8%uB2E4.%20%uC608%uC57D%uD558%uC2E0%20%uC0AC%uD56D%uC744%20%uD655%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694.", "gonexturl" : "/GolfRes/onepage/my_golfreslist.asp"}'
for i, tar in enumerate(re.split('[,:]', res)):
    if not tar:
        continue
    if i == 3:
        tar=tar.replace('%u', '\\u').encode().decode('unicode_escape')
    print(tar)