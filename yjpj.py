import base64
import re
import bs4
import requests

session = requests.Session()

nameBytes = base64.b64encode(bytes(input("请输入学号名：\n"), encoding='utf-8'))
pwd = base64.b64encode(bytes(input("请输入密码：\n"), encoding='utf-8'))
res = session.post("http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk", data={
    "encoded": nameBytes + b'%%%' + pwd
})
commentsExist = re.search(r'教学评价', res.text)
if not commentsExist:
    print("用户名或密码错误")
    exit()

soup = bs4.BeautifulSoup(
    session.get("http://csujwc.its.csu.edu.cn/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ").text, 'lxml')
if len(soup.find('table', class_="Nsb_r_list").findAll('tr')) < 2:
    print("暂无评教信息")
    exit()

commentsPageSoup = bs4.BeautifulSoup(session.get(
    "http://csujwc.its.csu.edu.cn" + soup.find('table', class_="Nsb_r_list").findAll('tr')[1].findAll('td')[6].a.attrs[
        'href']).text, 'lxml')

# 评分
comments = (commentsPageSoup.find('table', id="dataList").findAll('tr'))
for comment in comments:
    if comment.a:
        params = []
        commentPageSoup = bs4.BeautifulSoup(session.get(
            "http://csujwc.its.csu.edu.cn" + re.search(r"window\.open\('(.*)',1000,700\)",
                                                       comment.a.attrs['href']).group(1)).text, 'lxml').find('form')
        items = (commentPageSoup.find('table', id="table1").findAll('tr'))[1:-1]
        hiddenFields = commentPageSoup.findAll('input', type="hidden")
        for hiddenField in hiddenFields:
            params.append((hiddenField.attrs['name'], hiddenField.attrs['value']))
        items = (commentPageSoup.findAll('td', align="left"))
        for item in items:
            radioField = item.find('input', type="radio")
            params.append((radioField.attrs['name'], radioField.attrs['value']))
        params.append(('jynr',''))
        submitRes = session.post(url="http://csujwc.its.csu.edu.cn/jsxsd/xspj/xspj_save.do",
                                 data=params).text
        print(submitRes)

submitInputs = (commentsPageSoup.find("form", id="form1").findAll('input'))
submitParams = []
for submitInput in submitInputs:
    if 'name' in submitInput.attrs.keys():
        submitParams.append(
            (submitInput.attrs['name'],submitInput.attrs['value'])
        )

print(session.post("http://csujwc.its.csu.edu.cn/jsxsd/xspj/pltj_save.do",data=submitParams).text)