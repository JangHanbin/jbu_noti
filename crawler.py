import requests
from bs4 import BeautifulSoup


def shuttle_crawling():
    url = "http://www.joongbu.ac.kr/home/sub01_09_03.do"  # JBU Univ Shuttle bus information web page

    res = requests.get(url)

    html = res.text  # save response to html

    soup = BeautifulSoup(html, 'html.parser')  # parsing html(response html code) using html.parser

    routes = soup.select(
        '#content > table > tbody > tr'  # parsing this selector
    )

    for route in routes:
        route_str = route.text.split('\n')  # return list
        print(route_str)
        pivot = -1
        for i, line in enumerate(route_str):  # traverse list this routine must be has ':' in list
            if ':' in line and pivot == -1:
                pivot = i  # init pivot to i for find next seq values
                departure_time_index = route_str.index(line)  # save line(string) index
                departure_time = route_str[departure_time_index]  # save
                if route_str[departure_time_index - 1].isalpha():  # if there is route information in list
                    route_informaiton = route_str[
                        departure_time_index - 1]  # save bus route for using there is no route information in list

                # shuttlebus_info=[route_informaiton,departure_time,]
                # print(route_str[departure_time_index+1])
                # print(route_str[departure_time_index+1].isalpha())
                # print(route_str[departure_time_index+1].isalnum())
                # print(route_str[departure_time_index+1].isnumeric())
                # print(route_str[departure_time_index+1].isdigit())
                # print(route_str[departure_time_index+1])

            # print("Line : " + line)
            # print(pivot > -1)
            # print(':' not in line)
            # print(line.isalpha())
            # print("\n\n")
            if pivot > -1 and (':' not in line) and '' is not line:  # if pivot initialized
                location = line
                break

        print("노선명 : " + route_informaiton)
        print("탑승지 or 하차지 :  " + location)
        print("출발 시각 or 도착 시각 : " + departure_time)
        # print("가격  : " + price)
        # shuttlebus_info=[route_informaiton,departure_time,]
        print("\n\n")


def food_crawling():
    url = "http://www.joongbu.ac.kr/food/sub04_06_03/3.do"

    res = requests.get(url)

    html = res.text  # save response to html

    soup = BeautifulSoup(html, 'html.parser')  # parsing html(response html code) using html.parser

    dates = soup.select(
        '#content > table > thead > tr > th '  # parsing this selector
    )
    date_info = list()

    # parsing date
    for date in dates:
        if '/' in date.text:
            date_info.append(date.text)

    # parsing food menus
    foods = soup.select(
        '#content > table > tbody > tr > td'
    )

    find_section = False
    food1 = False
    food2 = False

    menus = dict(korean=[], food1=[], food2=[])
    for food in foods:
        if "석식" in food.text:
            break

        if find_section:
            if "일품2" in food.text:
                food2 = True
                continue # skip this text
            elif "일품1" in food.text:
                food1 = True
                continue # skip this text

            if not food1 and not food2:  # if korean food
                for newline in food.select("br"):  # replace <br> to space
                    newline.replace_with(" ")
                menus["korean"].append(food.text)
            elif food1 and food2: # if food2
                for newline in food.select("br"):  # replace <br> to space
                    newline.replace_with(" ")
                menus["food2"].append(food.text)
            elif food1 and not food2:  # if food1 and there is don't have to replace loop if they have more foods, then need to add replace loop
                menus["food1"].append(food.text)

        elif "한식" in food.text:
            find_section = True;

    return [date_info, menus]



# need to save route information & derparture time, price

if __name__ == '__main__':
    food_crawling()
# else:
#     print(__name__)
