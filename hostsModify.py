# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'yuan'
__mtime__ = '17-9-2'
__mail__ = kq_yuan@outlook.com

__description__== 将现有的hosts文件另存为hosts-日期 --> 从网络上下载最新的hosts文件保存为hosts

"""
import commands
import os
import time
import requests
import hashlib


def hosts_modify():
    # 检查是否为最新hosts文件
    url = "https://raw.githubusercontent.com/laucyun/hosts/master/hosts"
    try:
        response = requests.get(url)
        content = response.text
    except:
        print "Error while crawling the hosts files."
    content_md5 = hashlib.md5(content)
    with open("/etc/hosts", "r") as f:
        current_hosts = f.read()
    current_md5 = hashlib.md5(current_hosts)
    if current_md5.hexdigest() == content_md5.hexdigest():
        print "Your hosts is latest, nothing to update."
        return

    # 将原来的hosts另存为hosts-年月日时分秒
    new_filename = "hosts-" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    log_dir = "/etc/hosts-log/"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    if not os.path.isfile("/etc/" + new_filename) and os.path.isfile("/etc/hosts"):
        os.rename("/etc/hosts", log_dir + new_filename)

    # 更新hosts文件
    try:
        response = requests.get(url)
        content = response.text
    except:
        print "Error while crawling the hosts files."
    with open("/etc/hosts", "w") as f:
        f.write(content)

    # 替换 hosts 文件后，相关记录可能不会立即生效，可以关闭开启网络，或启用禁用飞行模式,让域名解析立即生效
    status, output = commands.getstatusoutput("systemctl restart NetworkManager")
    if status != 0:
        print "Unable restart NetworkManager"
        return

    print "Has restarted network, you can access https://scholar.google.com on your browser. \n However, you have to wait for a while."

if __name__ == '__main__':

    hosts_modify()

