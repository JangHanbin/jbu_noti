# -*- conding: utf-8 -*-


import os
from flask import Flask, request, jsonify
import busAPI
import crawler

app = Flask(__name__)


def TimeChk(time):
    return "도착 정보 없음" if not time else "{0}분 후 도착 예정".format(time)


def LocationChk(location):
    return " 정류장 정보 없음" if not location else " {0}전 ".format(location)


def Iswaiting(delay_info):
    return " 회차지 대기중 " if delay_info is "N" else ""


@app.route('/keyboard')
def Keyboard():
    send_data = {
        "type": "buttons",
        "buttons": ["시작하기", "도움말"]
    }

    return jsonify(send_data)


@app.route('/message', methods=['POST'])
def Message():
    received_data = request.get_json()
    content = received_data['content']

    if content == u"시작하기":
        send_data = {
            "message": {
                "text": "원하는 키워드를 보내주세요!\n"
                        "현재 PC카톡에서의 동작은 구현되지 않았습니다.\n"
                        "* 키워드는 \"도움말\"을 입력하세요 *"
            }
        }

    elif content == u"도움말":
        send_data = {
            "message": {
                "text": "아래의 text를 입력하시면 그에 맞는 답변이 전송됩니다!\n"
                        "'-2' 는 다음 배차에 대한 답변을 드립니다!\n"
                        "* 셔틀버스 시간표\n"
                        "* 033\n"
                        "* 033-2\n"
                        "* 054\n"
                        "* 054-2\n"
                        "* 학식 메뉴\n"
                        "* 건의 사항\n"

            }
        }
    elif (content == u"셔틀버스 시간표") or (content == u"셔틀 시간") or (content == u"셔틀") or (content == u"셔틀 시간표"):
        send_data = {
            "message": {
                "text": "요기다가 "
                        "각 시간을 넣으면"
                        "될것 같은데"
                        "현재시간을 파싱해서"
                        "가장 가까운 셔틀을 "
                        "출력해주는게 "
                        "좋겠따."
                        "셔틀은 홈페이지정보를 파싱했기때문에"
                        "부정확할수도있다고"
                        "말해줄것"
                        "그리고 노선이 너무 많으므로 "
                        "노선에 대한정보까지 입력받아 출력할 것"
            }
        }
    elif content == u"033" or (content == u"033-2"):
        bus_info = [busAPI.getBusArrivalTime("univ_front"),
                    busAPI.getBusArrivalTime("dormitory"),
                    busAPI.getBusArrivalTime("goyang-dong_market_033"),
                    busAPI.getBusArrivalTime("goyang-dong_market_to_subway")
                    ]
        if content == u"033":
            send_data = {
                "message": {
                    "text": "[중부대학교] -> [원흥역] \n* 첫차 시간 : " + bus_info[3][0] + "\n* 막차 시간 : " + bus_info[3][1] + "\n" +
                            "[원흥역] -> [중부대학교] \n* 첫차 시간 : " + bus_info[1][0] + "\n* 막차 시간 : " +bus_info[1][1] + "\n\n" +
                            "[중부대학교] -> [원흥역] :\n{0}{1}{2}".format(TimeChk(bus_info[0][2]), LocationChk(bus_info[0][6]), Iswaiting(bus_info[0][4])) + "\n\n\n" +
                            "[원흥연합기숙사] -> [중부대학교] :\n{0}{1}{2}".format(TimeChk(bus_info[1][2]), LocationChk(bus_info[1][6]), Iswaiting(bus_info[1][4])) + "\n\n\n" +
                            "[고양동 시장] -> [중부대학교] :\n{0}{1}{2}".format(TimeChk(bus_info[2][2]),LocationChk(bus_info[2][6]),Iswaiting(bus_info[2][4])) + "\n\n\n" +
                            "[고양동 시장] -> [원흥역] :\n{0}{1}{2}".format(TimeChk(bus_info[3][2]), LocationChk(bus_info[3][6]), Iswaiting(bus_info[3][4])) + "\n\n\n" 
                }
            }
        else:
            send_data = {
                "message": {
                    "text": "[중부대학교] -> [원흥역] \n* 첫차 시간 : " + bus_info[3][0] + "\n* 막차 시간 : " + bus_info[3][1] + "\n" +
                            "[원흥역] -> [중부대학교] \n* 첫차 시간 : " + bus_info[1][0] + "\n* 막차 시간 : " +bus_info[1][1] + "\n\n" +
                            "[중부대학교] -> [원흥역] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[0][3]), LocationChk(bus_info[0][7]), Iswaiting(bus_info[0][5])) + "\n\n\n" +
                            "[원흥연합기숙사] -> [중부대학교] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[1][3]), LocationChk(bus_info[1][7]), Iswaiting(bus_info[1][5])) + "\n\n\n" +
                            "[고양동 시장] -> [중부대학교] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[2][3]),LocationChk(bus_info[2][7]),Iswaiting(bus_info[2][5])) + "\n\n\n" +
                            "[고양동 시장] -> [원흥역] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[3][3]), LocationChk(bus_info[3][7]), Iswaiting(bus_info[3][5])) + "\n\n\n"
                }
            }
    elif content == u"054" or (content == u"054-2"):
        bus_info = [busAPI.getBusArrivalTime("goyang-dong_market_054"),
                    busAPI.getBusArrivalTime("univ_front_054"),
                    busAPI.getBusArrivalTime("univ_front_to_market"),
                    busAPI.getBusArrivalTime("gajang-dong_3-street")
                    ]
        if content == u"054":
            send_data = {
                "message": {
                    "text": "[고양동시장] -> [필리핀 참전비] \n* 첫차 시간 : " + bus_info[0][0] + "\n* 막차 시간 : " + bus_info[0][1] + "\n" +
                            "[필리핀 참전비] -> [고양동 시장] \n* 첫차 시간 : " + bus_info[3][0] + "\n* 막차 시간 : " + bus_info[3][1] + "\n" +
                            "[고양동시장] -> [필리핀 참전비] :\n{0}{1}{2}".format(TimeChk(bus_info[0][2]), LocationChk(bus_info[0][6]),Iswaiting(bus_info[0][4])) + "\n\n\n" +
                            "[중부대학교] -> [필리핀 참전비] :\n{0}{1}{2}".format(TimeChk(bus_info[1][2]), LocationChk(bus_info[1][6]), Iswaiting(bus_info[1][4])) + "\n\n\n" +
                            "[중부대학교] -> [고양동 시장] :\n{0}{1}{2}".format(TimeChk(bus_info[2][2]),LocationChk(bus_info[2][6]),Iswaiting(bus_info[2][4])) + "\n\n\n" +
                            "[관산동 삼거리]-> [고양동 시장(중부대학교)] :\n{0}{1}{2}".format(TimeChk(bus_info[3][2]), LocationChk(bus_info[3][6]), Iswaiting(bus_info[3][4])) + "\n\n\n"
                }
            }
        else:
            send_data = {
                "message": {
                    "text": "[고양동시장] -> [필리핀 참전비] \n* 첫차 시간 : " + bus_info[0][0] + "\n* 막차 시간 : " + bus_info[0][1] + "\n" +
                            "[필리핀 참전비] -> [고양동 시장] \n* 첫차 시간 : " + bus_info[3][0] + "\n* 막차 시간 : " + bus_info[3][1] + "\n" +
                            "[고양동시장] -> [필리핀 참전비] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[0][3]), LocationChk(bus_info[0][7]),Iswaiting(bus_info[0][5])) + "\n\n\n" +
                            "[중부대학교] -> [필리핀 참전비] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[1][3]), LocationChk(bus_info[1][7]), Iswaiting(bus_info[1][5])) + "\n\n\n" +
                            "[중부대학교] -> [고양동 시장] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[2][3]),LocationChk(bus_info[2][7]),Iswaiting(bus_info[2][5])) + "\n\n\n" +
                            "[관산동 삼거리]-> [고양동 시장(중부대학교)] 2번째 :\n{0}{1}{2}".format(TimeChk(bus_info[3][3]), LocationChk(bus_info[3][7]), Iswaiting(bus_info[3][5])) + "\n\n\n"
                }
            }
    elif (content == u"학식 메뉴") or (content == u"학식"):
        food_menus = crawler.food_crawling()
        send_data = {
            "message": {
                "text": "[{0} 메뉴] ".format(food_menus[0][0])+"\n" +
                        "<한식>\n" + food_menus[1]["korean"][0]+"\n" +
                        "<일품1>\n" + food_menus[1]["food1"][0]+"\n" +
                        "<일품2>\n" + food_menus[1]["food2"][0]+"\n"

            }
        }
    elif (content == u"건의 사항") or (content == u"건의") or (content == u"건의사항"):
        send_data = {
            "message": {
                "text": "Kakao Openchat URL : https://open.kakao.com/o/gFWkeII\n\n"
                        "Blog URL : http://dork94.tistory.com\n\n"
                        "Kakao ID : dorks"

            }
        }
    else:
        send_data = {
            "message": {
                "text": "* 찾으시려는 항목이 없습니다. *\n"
                        "\"도움말\"을 입력하여 가능한 도움말을 찾아보세요! "
            }
        }

    return jsonify(send_data)


# bus_Info["first_time", 0
# "last_time", 1
# "recent_arrival_time", 2
# "next_arrival_time", 3
# "recent_waiting_pot", 4
# "next_waiting_pot", 5
#  "recent_bus_station", 6
#  "next_bus_station"] 7

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2011)  # 0.0.0.0 mean allow all ip & port set to 2011
