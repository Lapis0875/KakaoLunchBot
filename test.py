from urllib.request import urlopen
import json


# 학교 급식 api 메뉴 사이트에서 급식메뉴 json 파일을 크롤링해온다. 해당 사이트 프로젝트 : https://github.com/5d-jh/school-menu-api
school_type = 'high'
school_code = 'B100000505'
year = 2019
month = 10
date = 7
URL = f'https://schoolmenukr.ml/api/{school_type}/{school_code}?year={year}&month={month}&date={date}'
result = json.loads(urlopen(URL).read().decode('utf-8'))
print(result, '\ntype = ', type(result))
menus = result["menu"][0]["lunch"]
print(menus, '\ntype = ', type(menus))
for menu in menus:
    print(menu)