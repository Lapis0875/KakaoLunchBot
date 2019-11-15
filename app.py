import json
from urllib.request import urlopen
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def yhkakaoskill():
    with open('kakao-skill.html', 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    return content


@app.route('/kakao-skill/<skillname>', methods=['POST', 'GET'])
def kakao_skill(skillname):
    if skillname == 'menu' and request.method == 'POST':
        r = request.json
        date = r['action']['params']['date']
        rd = json.loads(date.replace('/', ''))

        # 학교 급식 api 메뉴 사이트에서 급식메뉴 json 파일을 크롤링해온다. 해당 사이트 프로젝트 : https://github.com/5d-jh/school-menu-api
        school_type = 'high'
        school_code = 'B100000505'
        year, month, date = rd['value'].split('-')
        URL = f'https://schoolmenukr.ml/api/{school_type}/{school_code}?year={year}&month={month}&date={date}'

        result = json.loads(urlopen(URL).read().decode('utf-8'))
        menus = result["menu"][0]["lunch"]
        menu_today: str = ','.join(menus)

        response = {'version' : '1.0', 'template' : {'outputs' : [{'simpleText' : {'text' : menu_today}}]}}
        print(f'{r["block"]["name"]} : {r["user"]["id"]} requested menu skill. return value : {response}')

        return response
    elif skillname == 'menu' and request.method == 'GET':
        with open('kakao-skill/menu.html', 'rt', encoding='utf-8') as f:
            content = f.read()
            f.close()
        return content
    elif skillname == '' and request.method == 'GET':
        with open('kakao-skill.html', 'rt', encoding='utf-8') as f:
            content = f.read()
            f.close()
        return content
    else:
        return '<h1>WRONG ACCESS</h1>'


if __name__ == '__main__':
    app.run(port='80')
