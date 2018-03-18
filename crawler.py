import requests
from bs4 import BeautifulSoup


def shuttle_crawling():
    url = "http://www.joongbu.ac.kr/home/sub01_09_03.do"  # JBU Univ Shuttle bus information web page

    res = requests.get(url)

    html = res.text  # save response to html

    soup = BeautifulSoup(html, 'html.parser')  # parsing html(response html code) using html.parser

    routes = soup.select(
        '#content > table th'  # parsing this selector
    )
    table_column = list()
    column = list()
    for route in routes:
        # print(route.text.lstrip())
        column.append(route.text.strip())

        if 't_end' in route.get_attribute_list('class'):  # if end of the table column
            table_column.append(column.copy())  # need to value copy. default is address copy.
            column.clear()


    routes = soup.select(
        ' #content > table > tbody > tr '
    )

    row = list()
    time_table = list()
    rowspan_corrector = list()
    rowspan_list = list()

    for rowspan_idx , route in enumerate(routes):  # Parsing tables
        values = route.find_all('td')
        for value in values: # Parsing rows
            row.append(value.text.strip())   # add row
            if None not in value.get_attribute_list('rowspan'):     # if there is rowspan value
                rowspan_list.append([rowspan_idx, value.get_attribute_list('rowspan')[0], value.text.strip()])      # add rowspan information

        # each table Parsed
        time_table.append(row.copy())   # each row information save at list
        row.clear()     # clear list for save next row information
        if len(rowspan_list) > 0:   # if there is need to correct rowspan values
            rowspan_corrector.append(rowspan_list.copy())    # add to list
            rowspan_list.clear()    # clear list for next rowspan information
        else:
            rowspan_corrector.append("")  # add just trash value for match index

    #   column_rowspan[rowspan_idx, num_of_rowspan, text]
    for idx , table in enumerate(time_table):

        if len(rowspan_corrector[idx]) == 1:  # if there is just rowspan in column

            iterator = int(rowspan_corrector[idx][0][0])+1  # To avoid first rowspan value, because already set value in first rowspan
            span_idx = int(rowspan_corrector[idx][0][1])
            # print("Iterator : " + str(iterator) + " Span_idx : " + str(span_idx))
            while iterator < span_idx:
                # print(time_table[iterator])
                iterator+=1

            # print(rowspan_corrector[idx])
            # print(table)
        elif len(rowspan_corrector[idx]) > 1:  # if there is many rowspan in column
            print("")





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
                continue  # skip this text
            elif "일품1" in food.text:
                food1 = True
                continue  # skip this text

            if not food1 and not food2:  # if korean food
                for newline in food.select("br"):  # replace <br> to space
                    newline.replace_with(" ")
                menus["korean"].append(food.text)
            elif food1 and food2:  # if food2
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
    shuttle_crawling()
# else:
#     print(__name__)
