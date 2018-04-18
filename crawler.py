import requests
from bs4 import BeautifulSoup
import datetime

def ParsingCheaker(checker):
    do = 0  # checker index
    day = 1  # checker index

    today = datetime.datetime.now().day
    # Seems like Semaphore
    if today > checker[day]:  # if day goes by(check if need to parsing)
        checker[do] = True  # do Parsing
        checker[day] = datetime.datetime.now().day  # set to day by today
    else:
        checker[do] = False

    return checker[do]


def shuttle_crawling():
    url = "http://www.joongbu.ac.kr/home/sub01_09_03.do"  # JBU Univ Shuttle bus information web page

    res = requests.get(url)

    html = res.text  # save response to html

    soup = BeautifulSoup(html, 'html.parser')  # parsing html(response html code) using html.parser

    routes = soup.select(
        '#content > table > thead > tr'  # parsing this selector
    )
    table_column = list()
    column = list()

    for route in routes:
        route = route.find_all('th')
        for col in route:
            column.append(col.text.strip())

        # if end of the table column
        table_column.append(column.copy())  # need to value copy. default is address copy.
        column.clear()

    tables = soup.select(
        ' #content > table > tbody'
    )

    row = list()
    time_ = list()
    time_tables = list()
    rowspan_corrector = list()
    rowspan_correctors = list()
    rowspan_list = list()

    for table in tables:
        routes = table.find_all('tr')

        for route in routes:  # Parsing tables
            values = route.find_all('td')

            for rowspan_idx, value in enumerate(values):  # Parsing rows
                row.append(value.text.strip())  # add row

                if None not in value.get_attribute_list('rowspan'):  # if there is rowspan value
                    if '고양캠⇒충청캠' in value.text.strip() or '충청캠⇒고양캠' in value.text.strip():  # correct rowspan value set error! why jbu_univ web page that value set to 14??
                        rowspan_list.append([rowspan_idx, 1, value.text.strip()])  # add rowspan information
                    else:
                        rowspan_list.append([rowspan_idx, value.get_attribute_list('rowspan')[0], value.text.strip()])  # add rowspan information

            # each table_row Parsed
            time_.append(row.copy())  # each row information save at list
            row.clear()  # clear list for save next row information

            if len(rowspan_list) > 0:  # if there is need to correct rowspan values
                rowspan_corrector.append(rowspan_list.copy())  # add to list
                rowspan_list.clear()  # clear list for next rowspan information

            else:
                rowspan_corrector.append("")  # add just trash value for match index

        # each table parsed
        time_tables.append(time_.copy())
        time_.clear()
        rowspan_correctors.append(rowspan_corrector.copy())
        rowspan_corrector.clear()

    #   column_rowspan[rowspan_idx, num_of_rowspan, text]
    index_corrector = list()

    # correct(shift) index value & insert rowspan value as an order
    for idx, time_table in enumerate(time_tables):
        # idx is table number
        # ex) [[table1],[table2],[table3]]
        for c_idx, correctors in enumerate(rowspan_correctors[idx]):  # if there is need to correct time table
            # correctors is list of need to correct rowspan
            # ex) [[correct_list1],[correct_list2]]
            for correct_list in correctors:
                # correct_list is each list of need to correct
                # ex) [rowspan_idx, num_of_rowspan, text]
                corrected_index = correct_list[0]
                # check if need to correct insert index
                for index_correct in index_corrector:
                    # if same table num and belong to range & need to shift
                    if (idx == index_correct[0]) and (index_correct[1] < c_idx) and (index_correct[2] > c_idx) and (corrected_index >= index_correct[3]):
                        corrected_index += 1

                # index_corrector[table_num, range_of_start,range_of_end,corrected_idx]
                index_corrector.append([idx, c_idx, int(correct_list[1]) + c_idx, corrected_index])  # append correct info to correct index
                iterator = c_idx + 1  # To avoid first rowspan value, because already set value in first rowspan
                span_idx = c_idx + int(correct_list[1])  # From index of row to +num of rowspan

                # insert rowspan value into row
                while iterator < span_idx:
                    time_table[iterator].insert(corrected_index, correct_list[2])
                    iterator += 1


    return [table_column, time_tables]


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
