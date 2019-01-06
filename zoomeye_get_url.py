# -*- coding: utf-8 -*-
# @Time    : 2019-01-06 17:45
# @Author  : Hu3sky
# @FileName: zoomeye_get_url.py
# @Software: Submie

import os
import requests
import json

access_token = ''
ip_list = []
#你想要搜索的
query = input('[+] input : the data you want to search :')

def login():
    """
        输入用户名密码 进行登录操作
    :return: 访问口令 access_token
    """
    user = input('[+] input : username :')
    passwd = input('[+] input : password :')
    # 要搜索的字段
    data = {
        'username' : user,
        'password' : passwd
    }
    data_encoded = json.dumps(data)  # dumps 将 python 对象转换成 json 字符串
    try:
        r = requests.post(url = 'https://api.zoomeye.org/user/login',data = data_encoded)
        r_decoded = json.loads(r.text) # loads() 将 json 字符串转换成 python 对象
        global access_token
        access_token = r_decoded['access_token']
    except Exception as e:
        print('[+] info : username or password is wrong, please try again ')
        exit()
 
def saveStrToFile(file,str):
    """
        将字符串写入文件中
    :return:
    """
    with open(file,'w') as output:
        output.write(str)
 
def saveListToFile(file,list):
    """
        将列表逐行写入文件中
    :return:
    """
    s = '\n'.join(list)
    with open(file,'w') as output:
        output.write(s)
 
def apiTest():
    """
        进行 api 使用测试
    :return:
    """
    page = 1
    global access_token
    with open('access_token.txt','r') as input:
        access_token = input.read()
    # 将 token 格式化并添加到 HTTP Header 中
    headers = {
        'Authorization' : 'JWT ' + access_token,
    }
    # print(headers
    while(True):
        try:
            # query参数
            url = 'https://api.zoomeye.org/host/search?query={}&facet=app,os&page='.format(query)
            r = requests.get(url = url + str(page),headers = headers)
            r_decoded = json.loads(r.text)
            # print(r_decoded
            # print(r_decoded['total']
            for x in r_decoded['matches']:
                print(x['ip'])
                ip_list.append('http://'+x['ip'])
            print('[+] info : count ' + str(page * 10))
 
        except Exception as e:
            # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
            if str(e.message) == 'matches':
                print('[-] info : account was break, excceeding the max limitations')
                break
            else:
                print( '[+] info : ' + str(e.message))
        else:
            if page == 10:
                break
            page += 1
 
def main():
    # 访问口令文件不存在则进行登录操作
    if not os.path.isfile('access_token.txt'):
        print('[-] info : access_token file is not exist, please login')
        login()
        saveStrToFile('access_token.txt',access_token)
 
    apiTest()
    saveListToFile('ip_list.txt',ip_list)
 
if __name__ == '__main__':
    main()