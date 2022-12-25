# Importing the required modules
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup


def fall2022Average(p):
    # empty list
    data = []
    path = os.path.abspath(p)

    # for getting the header from
    # the HTML file
    list_header = []
    # with open(path, 'rb') as f:
    #     unicode_html = f.read().decode('utf-8', 'ignore')
    soup = BeautifulSoup(open(path, 'rb'), 'lxml')
    header = soup.find_all('table', {'class': 'table table-hover'})[0].find('tr')

    for items in header:
        try:
            list_header.append(items.get_text().replace('\n',''))
        except:
            continue

    # for getting the data
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text().replace('\n',''))
            except:
                continue
        data.append(sub_data)

    # Storing the data into Pandas
    # DataFrame
    dataFrame = pd.DataFrame(data=data, columns=list_header)

    df = dataFrame

    semesters = df.loc[:,"Semester"]
    index = -1
    indexes = []

    for s in semesters:
        index += 1
        if not s == 'Fall2022':
            continue
        indexes.append(index)

    grades = []

    for i in indexes:
        grades.append(float(df.loc[:, "Grade"][i]))

    print(sum(grades)/len(grades))

    dataFrame.to_csv(path+'.csv')



fall2022Average('./user.xls')