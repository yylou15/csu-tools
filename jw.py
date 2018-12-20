import csv
import re
from xml import etree

import requests
res = requests.get(
    url="http://csujwc.its.csu.edu.cn/"
)
myCookie = res.cookies
datas = {
    'encoded' : "?????????????????????"
    # 账号密码的base64加密结果
}
res = requests.post(
    url="http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk",
    cookies=myCookie,
    data=datas
)
# print(res.text)

# 打开文件
out = open('AllKc.csv', 'a', newline='', encoding='UTF-8')
csv_write = csv.writer(out, dialect='excel', )
csv_write.writerow(['课程', '学分','任课教师','职称','上课班级','上课班级名称','人数/班级','上课群组名称','行政班级','周次','节次','上课地点','承担单位'])


pageIndex = 150
while pageIndex<232:
    kcData = {
        "xnxqh": "2018-2019-2",
        "pageIndex": str(pageIndex)
    }

    print(pageIndex)
    res = requests.post(
        "http://csujwc.its.csu.edu.cn/jsxsd/kbcx/kbxx_kc_ifr",\
        cookies=myCookie,
        data=kcData
    )
    
    kcs = re.finditer(r'<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}<td>(.*?)</td>\r\n\t{2,3}', res.text)
    for i in kcs:
        # print(i.group(1) + i.group(2) + i.group(3))
        print(i.groups())
        csv_write.writerow(i.groups())
    
    pageIndex += 1

