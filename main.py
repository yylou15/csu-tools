import time

import requests
import bs4

from info import *

session = requests.Session()

soup = bs4.BeautifulSoup(session.post("http://ca.its.csu.edu.cn/Home/Login/215", data={
    "userName": studentId,
    "passWord": password,
    "enter": True
}).text, "lxml")

session.post("https://wxxy.csu.edu.cn/a_csu/api/sso/validate", data={
    "tokenId": soup.findAll("input")[0].attrs["value"],
    "account": soup.findAll("input")[1].attrs["value"],
    "Thirdsys": soup.findAll("input")[2].attrs["value"]
})

session.get("https://wxxy.csu.edu.cn/ncov/wap/default/index")

res = session.post("https://wxxy.csu.edu.cn/ncov/wap/default/save", data={
    "jcjgqr": "0",
    "tw": "3",
    "sfcxtz": "0",
    "sfjcbh": "0",
    "sfcxzysx": "0",
    "qksm": "",
    "sfyyjc": "0",
    "remark": "",
    "address": province + city + street + address,
    "geo_api_info": '',
    "area": "",
    "province": province,
    "city": "",
    "sfzx": "0",
    "sfjcwhry": "0",
    "sfjchbry": "0",
    "sfcyglq": "0",
    "gllx": "",
    "glksrq": "",
    "jcbhlx": "",
    "jcbhrq": "",
    "bztcyy": "",
    "sftjhb": "0",
    "sftjwh": "0",
    "jcjg": "",
    "uid": "uid",
    "created": time.time(),
    "date": time.strftime("%Y%m%d"),
    "id": "",
    "gwszdd": "",
    "sfyqjzgc": "",
    "jcqzrq": "",
    "sfjcqz": "",
    "jrsfqzys": "",
    "jrsfqzfy": "",
})
print(res.text)
