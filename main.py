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
                "text": "원하는 키워드를 보내주세요! * 키워드는 도움말을 입력하세요 *"
            }
        }

    elif content == u"도움말":
        send_data = {
            "message": {
                "text": "* 셔틀버스 시간표"
                        "* 033"
                        "* 054"
                        "* 학식 메뉴"
                        "* 건의 사항 "

            }
        }
    elif content == u"033":
        send_data = {
            "message": {
                "text": "중부대학교  ----> 원흥역행 도착 예정시간 API"
                        "원흥역     ----> 중부대학교행 도착 예정 시간 API"
                        "고양동 시장 ----> 중부대학교행 도착 예정 시간 API "
                        "고양동 시장 ----> 원흥역행 도착 예정 시간 API"

            }
        }
    elif content == u"054":
        send_data = {
            "message": {
                "text": "고양동시장  ----> 필리핀 참전비행 도착 예정시간 API"
                        "중부대학교  ----> 필리핀 참전비행 도착 예정시간 API"
                        "중부대학교  ----> 고양동 시장행 도착 예정시간 API"
                        "관산동 삼거리 ----> 고양동 시장(중부대학교)행 도착 예정시간 API"

            }
        }
    elif content == u"학식 메뉴":
        send_data = {
            "message": {
                "text": "오늘 학식 메뉴"
                        "요기다 학식 메뉴 넣어버리기~ "

            }
        }
    elif content == u"건의 사항":
        send_data = {
            "message": {
                "text": "Kakao Openchat URL : https://open.kakao.com/o/gFWkeII"
                        "Blog URL : http://dork94.tistory.com"
                        "Kakao ID : dorks"

            }
        }
    else:
        send_data = {
            "message": {
                "text": "* 찾으시려는 항목이 없습니다. 도움말을 입력하여 가능한 도움말을 찾아보세요! "
            }
        }

    return jsonify(send_data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000) #0.0.0.0 mean allow all ip & port set to 5000