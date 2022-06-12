
import csv
from heapq import merge
import os
import re

#
# Определение глобальных переменных и констант
#

RAW_FILENAME = 'phonebook_raw.csv'
NEW_FILENAME = 'phonebook.csv'

#
# Глобальные функции модуля
#

# функция загрузки адресной книги
def load_addrbook(filename: str) -> list:

    # проверяем наличие файла для загрузки токена
    if os.path.isfile(filename):
        # открываем файл и считываем данниые из файла csv
        with open(filename,  'r', encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
    else:
        # если файла не существует возвращаем пустой список
        contacts_list = []

    return contacts_list
# end load_addrbook

# функция проверки и корректировки ФИО
def check_fio(plist):
    # склеиваем все части ФИО, вне зависимости заполнены они или нет
    fio = plist[0] + ' ' + plist[1] + ' ' + plist[2]
    # разбиваем ФИО на Ф. И. О., с помощью регулярных выражений
    pattern = r'\w+'
    fio = re.findall(pattern, fio)
    # возвращаем корректный ФИО
    for i in range(len(fio)):
        plist[i] = fio[i]

# end check_fio

# функция проверки и исправления номера телефона
def check_phone(plist):
    
    #получаем номер телефона
    phone = plist[5]
    # если номер телефона указан, обрабатываем его
    if len(phone) > 0:
        # убираем все лишние символы "(", ")","+7","8","-" 
        pattern = r'^8 |^8|^\+[7] |^\+[7]|\(|\)|\-|\s'
        phone = re.sub(pattern, '', phone)
        # корректируем добавочный номер
        phone = phone.replace('доб.', ' доб.')
        phone = '+7(' + phone
        phone = phone[0:6] + ')' + phone[6:]
        phone = phone[0:10] + '-' + phone[10:]
        phone = phone[0:13] + '-' + phone[13:]
        # возвращаем обработанный номер телефона
        plist[5] = phone

# end check_phone


# функция упорядочения списка контактов
def normalize_addrbook(contacts_list: list):

    # исправляем каждую запись адресной книги
    for clst in contacts_list[1:]:
        # проверяем и исправляем корректность ФИО
        check_fio(clst)
        # проверяем и исправляем номер телефона
        check_phone(clst)

# end normalize_addrbook

# функция поиска одинаковых сотрудников в справочнике
def find_equal(lastname: str, firstname: str, clist: list) -> int:
    
    # поиск совпадений в списке
    i = 0
    for cl in clist:
        if lastname.upper() == str(cl[0]).upper() and firstname.upper() == str(cl[1]).upper():
            return i
        i += 1
    
    # совпадения не найдены
    return -1

# end find_equal

# функция объединения контактов
def merge_contacts(contact1: list, contact2: list):
    
    # объединяем элементы контактов
    for i in range(len(contact1)):
        if len(contact1[i]) < len(contact2[i]):
            contact1[i] = contact2[i]

# end merge_contacts

# функция объединения дублей записей адресной книги
def dedup_addrbook(contacts_list: list):
    
    i = 1
    while i < len(contacts_list):
        eq = find_equal(contacts_list[i][0], contacts_list[i][1], contacts_list[i+1:])
        if eq >= 0:
            eq = (eq + 1) + i
            merge_contacts(contacts_list[i], contacts_list[eq])
            del contacts_list[eq]
        i += 1

# end dedup_addrbook 

# функция сохранения адресной книги
def save_addrbook(filename: str, clist: list) -> int:

    # сохраняем результаты в csv файл
    with open(filename, "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(clist)

    return 0
# end save_addrbook

#
# Главная функция программы
#

def main():
    
    # загружаем из файла адресную книгу
    addrbook = load_addrbook(RAW_FILENAME)
    # если загрузка успешная 
    if len(addrbook) != 0:
        # исправляем адресную книгу
        normalize_addrbook(addrbook)
        # убираем дубли
        dedup_addrbook(addrbook)
        # сохраняем результат
        if save_addrbook(NEW_FILENAME, addrbook) < 0:
            print('Ошибка во время сохранения резульатов в файл: ', NEW_FILENAME)
    else:
        # если загрузка не удалась завершаем программу
        print('Файл ', RAW_FILENAME, 'не найден!')

# end main

#
# Основная программа
#

if __name__ == '__main__':
    main()
