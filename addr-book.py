
from audioop import add
import csv
import os

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
def check_fio(plst):
    pass
# end check_fio

# функция проверки и исправления номера телефона
def check_phone(plst):
    pass
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

# функция объединения дублей записей адресной книги
def dedup_addrbook(contacts_list: list):
    pass
# end dedup_addrbook 

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
    else:
        # если загрузка не удалась завершаем программу
        print('Файл ', RAW_FILENAME, 'не найден!')

# end main

#
# Основная программа
#

if __name__ == '__main__':
    main()
