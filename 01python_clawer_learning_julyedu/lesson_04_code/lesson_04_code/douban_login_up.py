import requests
import re
from bs4 import BeautifulSoup


s = requests.Session()
url_login = 'http://accounts.douban.com/login'

formdata = {
    'redir':'https://www.douban.com',
    'form_email': '674361437@qq.com',
    'form_password': '674361437ljf5221',
    'login': u'登陆'
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

r = s.post(url_login, data = formdata, headers = headers)
content = r.text
soup = BeautifulSoup(content, 'html.parser')
captcha = soup.find('img', id = 'captcha_image')
print(content)
if captcha:
    captcha_url = captcha['src']
    re_captcha_id = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captcha_id = re.findall(re_captcha_id, content)
    print(captcha_id)
    print(captcha_url)
    captcha_text = input('Please input the captcha:')
    formdata['captcha-solution'] = captcha_text
    formdata['captcha-id'] = captcha_id
    r = s.post(url_login, data = formdata, headers = headers)
with open('contacts.txt', 'w+', encoding = 'utf-8') as f:
    f.write(r.text)

