# import pandas as pd
# import main
import numpy as np
from statistics import mean

data_load = np.zeros(360 * 1440).reshape(360, 1440)
data = data_load.T[::4]
data = data_load.T[4::4]

step_y = None
step_x = None


def open_file(filepath, flag):
    global data_load  # Использование глобальной переменной
    global data  # Использование глобальной переменной
    data_load = np.genfromtxt(filepath, delimiter=',')[1::]  # Считывание файла
    data = data_load.T[::4]  # Выборка для датасета по градусам долготы
    data = data.T[4::4]  # Выборка для датасета по градусам широты
    # print(flag)
    if flag == 1:  # Если нажата кнопка
        return data  # Возврат не полного датасета
    else:  # Иначе
        return data_load  # Возврат полного датасета


def add_file(filepath, flag):
    global data_load  # Использование глобальной переменной
    global data  # Использование глобальной переменной
    add_data_load = np.genfromtxt(filepath, delimiter=',')[1::]  # Считывание файла
    add_data = add_data_load.T[::4]  # Выборка для датасета по градусам долготы
    add_data = add_data.T[4::4]  # Выборка для датасета по градусам широты
    if flag == 1:  # Если нажата кнопка
        for i in range(len(add_data)):
            for j in range(len(add_data.T)):
                data[i, j] = mean([add_data[i, j], data[i, j]])  # Усреднение значений
        return data  # Возврат не полного датасета
    else:
        for i in range(len(add_data_load)):
            for j in range(len(add_data_load.T)):
                data_load[i, j] = mean([add_data_load[i, j], data_load[i, j]])  # Усреднение значений
        return data_load  # Возврат полного датасета


def calculate_laplasian(flag):
    global data_load  # Использование глобальной переменной
    global data  # Использование глобальной переменной
    if flag == 1:  # Проверка на возврат датасета по градусам
        calculate_data = data.T[::step_x]  # Выборка по шагам для датасета по градусам долготы
        calculate_data = calculate_data.T[::step_y]  # Выборка по шагам для датасета по градусам широты
    else:
        calculate_data = data_load.T[::step_x]  # Выборка по шагам для датасета по градусам долготы
        calculate_data = calculate_data.T[::step_y]  # Выборка по шагам для датасета по градусам широты
    y_len, x_len = calculate_data.shape  # Запись длины массива по строкам и столбцам
    # Создание нового пустого массива
    data_laplas = np.empty(calculate_data.size, dtype=str).reshape(int(y_len), int(x_len))
    for i in range(y_len):
        for j in range(x_len):
            data_laplas[i, j] = 'X'  # Заполнение массива

    for i in range(1, y_len - 1):  # проход по столбцам, пропуская первые и последние записи
        for j in range(x_len):  # проход по строкам
            # расчёт лапласиан, если это последний номер строки
            if j >= x_len - 1:
                sub = (calculate_data[i - 1, j] + calculate_data[i, 0] + calculate_data[i, j - 1]
                       + calculate_data[i + 1, j]) - calculate_data[i, j] * 4
            else:  # расчёт лапласиан по формуле ([0,1]+[1,2]+[1,0]+[2,1]) - [1,1]*4
                sub = (calculate_data[i - 1, j] + calculate_data[i, j + 1] + calculate_data[i, j - 1]
                       + calculate_data[i + 1, j]) - calculate_data[i, j] * 4
            if sub < 0: data_laplas[i, j] = '-'  # если меньше нуля, то записываем "-"
            if sub > 0: data_laplas[i, j] = '+'  # если больше нуля, то "+"
            if sub == 0: data_laplas[i, j] = '0'  # если значения равны, то "0"
    return data_laplas  # возвращения нового массива с подсчитанными лапласианами
