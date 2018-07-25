"""
坦白说解密
@author: Bean.Wei
@data: 2018/07/25
"""

import io
import os 
import re
import time
import json
from random import random
import sys
import subprocess
import requests
from prettytable import PrettyTable

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gbk')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

sess = requests.Session()
sess.proxies = {"http":"127.0.0.1:8080"}
QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'webQQqr.png'


def login():
    """登录QQ"""
    getQR()
    while True:
        resp, code = scanQR()
        if code == '0':
            break
    #删除二维码
    os.remove(QRImgPath)
    qq = re.findall(r'(?<=uin=).*?(?=&service)',resp.text)[0]
    print(qq,'登陆成功')
    skey = sess.cookies['skey']
    print('正在获取坦白说...')

    tanbai_url = 'https://ti.qq.com/cgi-node/honest-say/receive/mine?_client_version=2.3.5&_t=1531303725632&token='+genbkn(skey)
    tanbai = sess.get(tanbai_url,headers = headers,timeout=1000)
    print(tanbai.json())
    tanbai_EncodeUin = re.findall(r'"fromEncodeUin":"(.+?)"',tanbai.text)
    tanbai_topicName = re.findall(r'"topicName":"(.+?)"',tanbai.text)

    row = PrettyTable()
    row.field_names = ["QQ","备注","坦白说"]
    i = 0
    qzone_url = 'https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/user/cgi_personal_card?uin='
    while i<len(tanbai_EncodeUin):
        if len(tanbai_EncodeUin[i])==28:
            num = genqq(tanbai_EncodeUin[i].replace('*S1*',''))
        else:
            num = genqq(tanbai_EncodeUin[i].replace('*S1*',''))
        if len(num)==18:
            json=post(num)
            miwen=json['result']['ss_uin']
            print(miwen)
            friendrealqq =genqq(miwen.replace('*S1*',''))
            print(friendrealqq)
            print('-'*50)
        else:
            friendrealqq=num
            print(friendrealqq)
            print('-'*50)
            
        tanbai = tanbai_topicName[i]
        try:
            user_qzone = qzone_url + friendrealqq + '&g_tk=' + genbkn(skey)
            resp = sess.get(user_qzone,headers = headers)
            nick =  re.findall(r'"realname":"(.+?)"',resp.text)[0]
            row.add_row([friendrealqq,nick,tanbai])
            i = i + 1
        except:
            nick=' '
            row.add_row([friendrealqq,nick,tanbai])
            i=i+1
            continue
        
    print(row)

def getQR():
    """获取QZone登录二维码"""
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
    params = {
                'appid': '549000912',
                'e': '2',
                'l': 'M',
                's': '3',
                'd': '72',
                'v': '4',
                't': '%.17f' % (random()),
                'daid': '5',
                'pt_3rd_aid': 0}
    qrresp = sess.get(url, params=params, timeout=1000)
    with open(QRImgPath, 'wb') as f :
        f.write(qrresp.content)
        f.close()

    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', QRImgPath])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', QRImgPath])
    else:
        os.startfile(QRImgPath)
    print(u'请使用手机 QQ 扫描二维码以登录')

def scanQR():
    """确认登录"""
    qrsig = sess.cookies['qrsig']
    url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
    params = {
            'u1': 'https://qzs.qzone.qq.com/qzone/v5/loginsucc.html',
            'para': 'izone',
            'ptqrtoken': genqrtoken(qrsig),
            'ptredirect': '1',
            'h': '1',
            't': '1',
            'g': '1',
            'from_ui': '1',
            'ptlang': '2052',
            'action': '0-0-%d' % (time.time() * 1000),
            'js_ver': '10276',
            'js_type': '1',
            'pt_uistyle': '40',
            'aid': '549000912',
            'daid': '5'}
    resp = sess.get(url, params=params, timeout=1000,headers = headers)
    code = re.findall(r'(?<=ptuiCB\(\').*?(?=\',)',resp.text)[0]
    if code == '67':
        print('扫码成功，请确认登录')
    if code == '0' :
        print('确认登陆成功')
    elif code == '65' :
        print('二维码失效, 请重新启动程序')
    return resp, code 

def post(uid):
    PostUrl = "https://nearby.qq.com/cgi-bin/nearby/web/card/get_score_page_info"
    postData = {'enumn_type':'1',
                'latitude':'0',
                'longitude':'0',
                'portal':'2',
                'client_type':'2',
                'list_size':'10',
                'gender':'0',
                'client_version':'0',
                'tinyid':uid,
                'bkn':'344613249'}
    #datas = urllib.parse.urlencode(postData).encode(encoding='UTF-8')
    response = sess.post(PostUrl,headers=headers,data=postData,proxies =sess.proxies,timeout=10)
    print(response.json())
    return response.json()

def recookies(s):
    s=s.replace('=',':')
    l=s.split('; ')
    d=[]
    for i in range(len(l)):
        l1=l[i].split(':')
        if len(l1)==3:
            l1.remove('pgv_info')
        d.append(l1)
    return dict(d)

def genqrtoken(qrsig):
    e = 0
    for i in range(0, len(qrsig)):
        e += (e << 5) + ord(qrsig[i])
    qrtoken = (e & 2147483647)
    return str(qrtoken)

def genbkn(skey):
    b = 5381
    for i in range(0, len(skey)):
        b += (b << 5) + ord(skey[i])
    bkn = (b & 2147483647)
    return str(bkn)

def genqq(qq):
    a=qq
    d = {"oe": 0, "n": 0, "z": 0, "on": 0,
         "oK": 1, "6": 1, "5": 1, "ov": 1,
         "ow": 2, "-": 2, "A": 2, "oc": 2,
         "oi": 3, "o": 3, "i": 3, "oz": 3,
         "7e": 4, "v": 4, "P": 4, "7n": 4,
         "7K": 5, "4": 5, "k": 5, "7v": 5,
         "7w": 6, "C": 6, "s": 6, "7c": 6,
         "7i": 7, "S": 7, "l": 7, "7z": 7,
         "Ne": 8, "c": 8, "F": 8, "Nn": 8,
         "NK": 9, "E": 9, "q": 9, "Nv": 9}
    l = 4
    ans = ''
    
    e=[]
    for j in [0,4,8,12,16,20]:
        e.append(qq[j:j+4])
    for k in range(len(e)):
        s=e[k]
        i = 0
        if s == None:
            break
        while (i <len(s) ):
            
            if i+1 < l:
                x = s[i]+s[i+1]
                if x in d.keys():
                    ans = ans+str(d[x])
                    i = i+2
                    
            if a[i] in d.keys() and i<len(s):
                ans = ans+str(d[s[i]])
                i = i+1
        k = k+1
    return ans

if __name__ == "__main__":
    login()