import csv
import re

# Читаем исходный файл phonebook_raw.csv
with open("phonebook_raw.csv", encoding='utf-8') as file:
    contacts_list = list(csv.reader(file, delimiter=','))

for line in contacts_list:
    list_line = []  # Список имя, фамилия, отчество
    for part in line[0:3]:
        if part:
            list_line.extend(part.split(' '))
    list_line = list_line + [''] * (3 - len(list_line))
    line[:3] = list_line  # Вставляем список ФИО в поля lastname, firstname и surname исходного списка contacts_list

    # Приводим все телефоны в формат +7(999)999-99-99. Если есть добавочный номер: +7(999)999-99-99 доб.9999
    final_phone = re.sub(r"(\+7|8)\W*(\d{3})\W*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})",
                         r"+7(\2)\3-\4-\5", line[5])
    phone = re.sub(r"\(*доб.\s*(\d{4})\)*", r"доб.\1", final_phone)
    line[5] = phone  # Вставляем исправленный номер в поле phone списка contacts_list
print(contacts_list)

final_contacts = []  # Финальный список
final_contacts.append(contacts_list[0])  # Добавляем список названий полей в финальный список
index_list = []  # Список индексов отработанных элементов списка contacts_list

for index in range(1, len(contacts_list)):
    line = contacts_list[index]
    # Список индексов элементов списка contacts_list с совпадающими фамилия, имя
    identical_list = [n for n, j in enumerate(contacts_list) if j[:2] == line[:2]]
    list_1 = ['' for i in range(len(line))]  # Список, заполненный пустыми строками
    for num_identical in identical_list:
        if num_identical not in index_list:  # Если индекса нет в списке index_list
            # Промежуточный список куда вставлены значения из очередного списка с совпадающими фамилия, имя
            list_2 = [(contacts_list[num_identical][i] if list_1[i] == '' else list_1[i]) for i in range(len(list_1))]
            list_1 = list_2  # Вставляем промежуточный список в список, заполненный пустыми строками
            index_list.append(num_identical)  # Добавляем отработанный индекс в список index_list
    if list_1 != ['' for i in range(len(line))]:  # Если получившийся список заполнен значениями
        final_contacts.append(list_1)  # Добавляем его в финальный список
print(final_contacts)

# Записываем финальный список final_contacts в файл phonebook.csv
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts)
