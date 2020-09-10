import json
import re
import sys

import bs4
import requests

session = requests.Session()
soup = bs4.BeautifulSoup(session.post("http://ca.its.csu.edu.cn/Home/Login/215", data={
    "userName": sys.argv[1],
    "passWord": sys.argv[2],
    "enter": True
}).text, "lxml")

session.post("https://wxxy.csu.edu.cn/a_csu/api/sso/validate", data={
    "tokenId": soup.findAll("input")[0].attrs["value"],
    "account": soup.findAll("input")[1].attrs["value"],
    "Thirdsys": soup.findAll("input")[2].attrs["value"]
})

main_page = session.get("https://wxxy.csu.edu.cn/ncov/wap/default/index?from=history").text
info = json.loads(re.search(r'var\sdef\s=(.*);', main_page).group(1).strip())
address_info = json.loads(info['geo_api_info'])['addressComponent']
info['szgj'] = address_info['country']
info['szcs'] = address_info['city']
info['szgjcs'] = "{} {}".format(address_info['country'], address_info['city'])
info['area'] = "{} {} {}".format(address_info['province'], address_info['city'], address_info['district'])

res = json.loads(session.post("https://wxxy.csu.edu.cn/ncov/wap/default/save", data=info).text)
print("打卡结果：{}，上次打卡地点：{}".format(res['m'], json.loads(info['geo_api_info'])['formattedAddress']))
