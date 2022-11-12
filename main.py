from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
from typing import List

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

pattern = "(\+7|8)\s?\(?(\d{3})\)?(-|\s)?(\d{3})-?(\d{2})-?(\d+)"

lastname_list = []
lastname_merge = []
for person in contacts_list:
    lastname = person[0].split(' ')
    name = person[1].split(' ')
    if len(lastname) == 3:
        person[0] = lastname[0]
        person[1] = lastname[1]
        person[2] = lastname[2]
    elif len(lastname) == 2:
        person[0] = lastname[0]
        person[1] = lastname[1]
    if len(name) == 2:
        person[1] = name[0]
        person[2] = name[1]
    if "доб" in person[-2]:
        pattern_add = "\(?\w+\.\s(\d{4})\)?"
        result_add = re.sub(pattern_add, r"доб.\1", person[-2])
        print(result_add)
        person[-2] = result_add

    result = re.sub(pattern, r"+7(\2)\4-\5-\6", person[-2])
    person[-2] = result
    lastname_list.append(person[0])

for person in contacts_list:
    if lastname_list.count(person[0]) > 1:
        print(person[0])
        lastname_merge.append(person[0])
lastname_merge_fin = list(set(lastname_merge))

list_del = []

for l_name in lastname_merge_fin:
    person_zip = ['','','','','','','']
    for person in contacts_list:
        if person[0] == l_name:
            person_new = ['','','','','','','']
            print('до: ', person_new)
            for k in range(7):
                if person[k] in person_zip[k]:
                    person_new[k] = ''
                else:
                    person_new[k] = person[k]
                print(f'person_new[{k}]= {person[k]}')
            person_zip_new = [x + y for x, y in zip(person_new, person_zip)]
            person_zip = person_zip_new
            list_del.append(person)

    contacts_list.append(person_zip)

for element in list_del:
    contacts_list.remove(element)

pprint(contacts_list)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
