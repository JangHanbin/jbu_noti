# coding : utf8

import json
import requests

def getBusArrivalTime(station_name):
    # Gyeong-gi Bus information API web page
    url = "http://www.gbis.go.kr/gbis2014/schBusAPI.action"
    
    station = {"home_front": ["054", "218000816"],
               "goyang-dong_market_054": ["054", "218000050"],
               "goyang-dong_market_033": ["033", "218000050"],
               "goyang-dong_market_to_subway": ["033", "218000177"],
               "univ_front": ["033", "218000812"],
               "univ_front_054": ["054", "218000812"],
               "univ_front_to_market": ["054", "218000811"],
               "gajang-dong_3-street": ["054","218001318"],
               "dormitory": ["033", "218001324"]
               }

    payload = {"cmd": "searchBusStationJson", "stationId": station[station_name][1]}

    res = requests.post(url, data=payload)
    # print(res.text)
    json_data = json.loads(res.text)
    
    # bus_Info["first_time",
    # "last_time",
    # "recent_arrival_time",
    # "next_arrival_time",
    # "recent_waiting_pot_bool",
    # "next_waiting_pot_bool",
    # "recent_bus_station",
    # "next_bus_station"]
    
    for busArrivalInfo in json_data["result"]["busArrivalInfo"]:
        if busArrivalInfo["routeName"] == station[station_name][0]:
            bus_info = [busArrivalInfo["firstTime"],
                        busArrivalInfo["lastTime"],
                        busArrivalInfo["predictTime1"],
                        busArrivalInfo["predictTime2"],
                        busArrivalInfo["delayYn1"],
                        busArrivalInfo["delayYn2"],
                        busArrivalInfo["locationNo1"],
                        busArrivalInfo["locationNo2"],
                        ]
    return bus_info


if __name__ == '__main__':
    getBusArrivalTime("home_front")
