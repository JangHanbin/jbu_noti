# coding : utf8

import json
import requests


def getBusArrivalTime(station_name):
    # Gyeong-gi Bus information API web page
    url = "http://www.gbis.go.kr/gbis2014/schBusAPI.action"
    
    station = {"home_front": ["054", "218000816"],
               "goyang-dong_market_054": ["054", "218000050"],
               "goyang-dong_market_033": ["033", "218000050"],
               "univ_front": ["033", "218000812"],
               "univ_front_to_market": ["054", "218000811"],
               "gajang-dong_3-street": ["054","218001318"]
    
               }

    payload = {"cmd": "searchBusStationJson", "stationId": station[station_name][1]}
    
    # custom_headers = {
    #     'Accept': 'application/json, text/javascript, */*; q=0.01',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'Connection': 'keep-alive',
    #     'Content-Length': '44',
    #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'Cookie': 'PHAROSVISITOR=00001a1501621ff6fed96928c0a867c9; ACEFCID=UID-5AA7EEBFE218CF2078DC4B1F; myword=054; '
    #               'JSESSIONID=em8IFcVQmU4umyZoLjLdfkculLoQuqWXvPACDF3POj9aUa7PMhWi8hjWLrOyN3tL.Gbus-WAS_servlet_engine4',
    #     'Origin': 'http://www.gbis.go.kr',
    #     'Referer': 'http://www.gbis.go.kr/gbis2014/schBus.action?cmd=mainSearchText&gubun=main',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/64.0.3282.186 Safari/537.36',
    #     'X-Requested-With': 'XMLHttpRequest'
    # }
    
    res = requests.post(url, data=payload)
    # print(res.text)
    json_data = json.loads(res.text)
    
    # bus_Info["first_time",
    # "last_time",
    # "recent_arrival_time",
    # "next_arrival_time",
    # "recent_waiting_pot_bool",
    # "next_waiting_pot_bool",
    #  "recent_bus_statiton",
    #  "next_bus_station"]
    
    for busArrivalInfo in json_data["result"]["busArrivalInfo"]:
        if busArrivalInfo["routeName"] == "054":
            bus_info = [busArrivalInfo["firstTime"],
                        busArrivalInfo["lastTime"],
                        "도착 정보 없음" if not busArrivalInfo["predictTime1"] else busArrivalInfo["predictTime1"],
                        "회차지 대기 중 ", "회차지 대기 중" if busArrivalInfo["delayYn1"] is "N" else "",
                        "두번째 차량 회차지 대기 중" if busArrivalInfo["delayYn2"] is "N" else ""]
    return bus_info


if __name__ == '__main__':
    getBusArrivalTime("home_front")
