import json
from urllib.request import urlopen
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    with open('server/index.html', 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    return content


@app.route('/lunchmenu', methods=['POST'])
def lunchmenu():
    data = request.get_json()
    print(f'data = {data}')

    requestdata = open('latest_request.json', 'wt')
    requestdata.write(str(data).replace("'", '"'))
    requestdata.close()

    print(f'data["bot"]["name"] = {data["bot"]["name"]}')
    if data['bot']['name'] == '영훈고챗봇':
        print('유저가 챗봇을 통해 요청을 보냈음.')
        time = data['action']['detailParams']['date']['origin']
    elif data['bot']['name'] == '봇 이름':
        print('테스트 서버 응답으로 확인함.')
        time = data['action']['params']['date']
    else:
        # 잘못된 요청에 따른 응답 메세지 전송 후 스킬 종료.
        response_body = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': '잘못된 요청입니다. 만약 일반 사용자가 이러한 문구를 보고 있다면, 개발자가 오류를 해결할 수 있도록 알려주세요. '
                        }
                    }
                ]
            }
        }
        res = jsonify(response_body)
        res.headers['Content-type'] = 'application/json; charset=utf-8'
        return res

    print(f'time : {time}')
    # 학교 급식 api 메뉴 사이트에서 급식메뉴 json 파일을 크롤링해온다. 해당 사이트 프로젝트 : https://github.com/5d-jh/school-menu-api
    school_type = 'high'
    school_code = 'B100000505'
    year, month, date = time.split('-')
    URL = f'https://schoolmenukr.ml/api/{school_type}/{school_code}?year={year}&month={month}&date={date}'
    print(f'URL = {URL}')

    result = json.loads(urlopen(URL).read())
    print(f'result = {result}')
    menus = result["menu"][0]["lunch"]
    menu_today: str = ','.join(menus)
    print(f'menu_today = {menu_today}')

    if menu_today == '':
        import random
        menu_today += random.choice(['오늘은 급식이 없어요!','오늘은 학교에서 급식을 제공하지 않는 날입니다!'])

    # 응답 설정.
    response_body = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': menu_today
                    }
                }
            ]
        }
    }
    print(f'response = {response_body}')
    response = jsonify(response_body)
    # res.headers['Content-type'] = 'application/json; charset=utf-8'
    return response


@app.route('/schedule', methods=['POST'])
def schedule():
    req = request.get_json()
    print(f'data = {req}')

    print(f'data["bot"]["name"] = {req["bot"]["name"]}')
    if req['bot']['name'] == '영훈고챗봇':
        print('유저가 챗봇을 통해 요청을 보냈음.')
        time = req['action']['detailParams']['date']['origin']
    elif req['bot']['name'] == '봇 이름':
        print('테스트 서버 응답으로 확인함.')
        time = req['action']['params']['date']
    else:
        # 잘못된 요청에 따른 응답 메세지 전송 후 스킬 종료.
        res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': '잘못된 요청입니다. 만약 일반 사용자가 이러한 문구를 보고 있다면, 개발자가 오류를 해결할 수 있도록 알려주세요. '
                        }
                    }
                ]
            }
        }
        return jsonify(res)

    # 응답 설정.
    res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': f'grade = {}, class = {} '
                        }
                    }
                ]
            }
        }
    
    print(f'response = {res}')
    return jsonify(res)


if __name__ == '__main__':
    app.run(port=5000)
