# -*- conding: utf-8 -*-


import os
from flask import Flask, request, jsonify



app = Flask(__name__)


@app.route('/keyboard')
def Keyboard():

    send_data = {
        "type"  :   "buttons",
        "buttons"   : ["시작하기", "도움말"]
    }

    return jsonify(send_data)


@app.route('/message', methods=['POST'])
def Message():

    received_data= request.get_json()
    content = received_data['content']

    if content == u"시작하기":
        send_data = {
            "message": {
                "text": "원하는 키워드를 보내주세요!\n"
                        "* 키워드는 도움말을 입력하세요 *"
            }
        }

    elif content == u"도움말":
        send_data = {
            "message": {
                "text": "* 셔틀버스 시간표\n"
                        "* 033\n"
                        "* 054\n"
                        "* 학식 메뉴\n"
                        "* 건의 사항\n"

            }
        }
    elif content == u"033":
        send_data = {
            "message": {
                "text": "중부대학교  ----> 원흥역행 도착 예정시간 API\n"
                        "원흥역     ----> 중부대학교행 도착 예정 시간 API\n"
                        "고양동 시장 ----> 중부대학교행 도착 예정 시간 API\n"
                        "고양동 시장 ----> 원흥역행 도착 예정 시간 API\n"

            }
        }
    elif content == u"054":
        send_data = {
            "message": {
                "text": "고양동시장  ----> 필리핀 참전비행 도착 예정시간 API\n"
                        "중부대학교  ----> 필리핀 참전비행 도착 예정시간 API\n"
                        "중부대학교  ----> 고양동 시장행 도착 예정시간 API\n"
                        "관산동 삼거리 ----> 고양동 시장(중부대학교)행 도착 예정시간 API\n"

            }
        }
    elif content == u"학식 메뉴":
        send_data = {
            "message": {
                "text": "오늘 학식 메뉴 \n"
                        "요기다 학식 메뉴 넣어버리기~ "

            }
        }
    elif content == u"건의 사항":
        send_data = {
            "message": {
                "text": "Kakao Openchat URL : https://open.kakao.com/o/gFWkeII\n"
                        "Blog URL : http://dork94.tistory.com\n"
                        "Kakao ID : dorks\n"

            }
        }
    else:
        send_data = {
            "message": {
                "text": "* 찾으시려는 항목이 없습니다. *\n"
                        "도움말을 입력하여 가능한 도움말을 찾아보세요! "
            }
        }

    return jsonify(send_data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 2011) #0.0.0.0 mean allow all ip & port set to 2011