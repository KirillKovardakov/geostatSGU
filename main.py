import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
import algorithm as alg


def changeFormat():
    if radio_state.get() == 0:
        root.attributes("-fullscreen", True)
        add_file_button.grid(row=1, column=1)
        check_button.grid(row=0, column=1)
        label_step1.grid(row=2, column=1)
        entry1.grid(row=2, column=2)
        label_step2.grid(row=3, column=1)
        entry2.grid(row=3, column=2)
        send_button.grid(row=4, column=2)
        laplasian_button.grid(row=5, column=1)
        text_editor.grid()
        scrollerX.grid()
        scrollerY.grid()
        open_button.grid()
        save_buttonCSV.grid()
        back_button.grid()
    elif radio_state.get() == 1:
        root.attributes("-fullscreen", False)
        root.geometry('500x300')
        add_file_button.grid(row=0, column=0)
        check_button.grid(row=0, column=1)
        label_step1.grid(row=1, column=0)
        entry1.grid(row=1, column=1)
        label_step2.grid(row=2, column=0)
        entry2.grid(row=2, column=1)
        send_button.grid(row=3, column=1)
        laplasian_button.grid(row=3, column=1)
        text_editor.grid_remove()
        scrollerX.grid_remove()
        scrollerY.grid_remove()
        open_button.grid_remove()
        save_buttonCSV.grid_remove()
        back_button.grid_remove()


def func_help():
    Label(tkinter.Toplevel(root), justify=LEFT, font=('Arial', 14), text='''
    Для начала работы с программой необходимо добавить файл расширения CSV, нажав кнопку "Открыть файл". 
    Файл должен быть получен путём экспорта из приложения panoply (В нём вы также добавляете файл с раширением nc, 
    затем нажимаете File -> Export as -> CSV).
    Вы можете поставить галочку "Расчет по градусам", чтобы объём данных уменьшился в 4 раза.
    Если есть необходимость расчета средних полей разных датасетов, нужно нажать кнопку "Добавить файл".
    Программа автоматически подсчитает средние поля и выведет в форму текста. 
    Следующим шагом является задание шагов отбора данных по широте и долготе. Необходимо ввести целочисленные числа,
    являющиеся делителями размера данных (360 на 1440 или 90 на 360).
    После того, как будут заданы шаги, откроется кнопка "Подсчитать лапласианы". Нажимаем на неё и видим результаты.
    После рассчёта лапласиан, данные можно сохранить с расширением CSV, нажав кнопу "Сохранить как CSV".
    Также можно изменить размер окна приложения в меню. В меньшей версии не будет вывода данных на экран.
    ''').grid()


def aboutProgram():
    about = tkinter.Toplevel(root)
    Label(about, text='''
    version 1.0
    Приложение сделано в 2023 году при помощи
    Python 3.9.7 и GUI tkinter.
    Для студентов Географического факультета 
    Саратовского государственного университета
    Имени Н. Г. Чернышевского.
    Разработано студентом 4 курса факультета 
    КНиИТ, направление ИВТ.
    Ссылка на разработчика:
    https://github.com/KirillKovardakov''').grid()


def print_text(args):
    text_editor.delete("1.0", END)  # Удаляем предыдущие записи
    for string in args:
        for j in range(len(string)):
            if j != len(string) - 1:  # Если это последний элемент, то записывается без пробела
                text_editor.insert(END, str(string[j]) + ' ')  # Записываем поэлементно в конец формы
            else:
                text_editor.insert(END, str(string[j]))
        text_editor.insert(END, '\n\n')  # Добавляем два переноса строки для визуального восприятия


# открываем файл в текстовое поле
def open_file():
    filepath = filedialog.askopenfilename()  # Запрос на открытие файла
    if filepath == "":  # Если путь пустой, то вывод ошибки
        mb.showerror(
            "Ошибка",
            "Необходимо выбрать файл")
    elif filepath[-3::] != "csv":  # Проверка файла на расширение CSV
        mb.showerror(
            "Ошибка",
            "Необходимо выбрать файл")
    else:
        if radio_state.get() == 0:
            print_text(alg.open_file(filepath, checkFlag.get()))  # Вывод данных в форму текста
        else:
            alg.open_file(filepath, checkFlag.get())
        add_file_button['state'] = 'normal'  # Установка кнопки в активное состояние


# добавляем файл для расчёта средних полей
def add_file():
    filepath = filedialog.askopenfilename()  # Запрос на открытие файла
    if filepath == "":  # Если путь пустой, то вывод ошибки
        mb.showerror(
            "Ошибка",
            "Необходимо выбрать файл")
    elif filepath[-3::] != "csv":  # Проверка файла на расширение CSV
        mb.showerror(
            "Ошибка",
            "Необходимо выбрать файл")
    else:
        if radio_state.get() == 0:
            print_text(alg.add_file(filepath, checkFlag.get()))  # Вывод данных в форму текста
        else:
            alg.add_file(filepath, checkFlag.get())


# функция для кнопки отправки данных
def send_steps():
    x = entry1.get()  # Получаем введенный шаг для широты
    y = entry2.get()  # Получаем введенный шаг для долготы
    if not x.isdigit() or not x.isdigit():  # Проверка на то, что введено число
        mb.showwarning(
            "Предупреждение",
            "Внимание: Введенное значение должно быть целым числом")
    elif int(x) <= 0 or int(y) <= 0:  # Проверка на корректность шага
        mb.showwarning(
            "Предупреждение",
            "Внимание: Числа должны быть больше 0")
    elif len(alg.data_load) % int(x) != 0:  # Проверка первого шага на делимость
        mb.showerror(
            "Ошибка",
            "Число 1 не является делителем")
    elif len(alg.data_load.T) % int(y) != 0:  # Проверка второго шага на делимость
        mb.showwarning(
            "Ошибка",
            "Число 2 не является делителем")
    else:  # Запись шагов и установка активности для кнопки
        alg.step_x = int(entry1.get())
        alg.step_y = int(entry2.get())
        laplasian_button['state'] = 'normal'


# Функция расчёта лапласиан
def calculate():
    if alg.data_load.all() == 0:  # проверка что есть данные
        mb.showerror(  # Если нет данных, то вывод сообщения об ошибки
            "Ошибка",
            "Необходимо выбрать файл с данными")
    elif alg.step_x is not None or alg.step_y is not None:  # проверка, что указаны шаги выборки
        print_text(alg.calculate_laplasian(checkFlag.get()))
    else:  # Если шаги не заданы, то вывод сообщения об ошибки
        mb.showerror(
            "Ошибка",
            "Не заданы шаги выборки")


# сохраняем текст из текстового поля в файл
def save_fileCSV():
    filepath = filedialog.asksaveasfilename() + '.csv'  # Получении места сохранения файла в формате .CSV
    if filepath != "":  # Если путь к файлу не пустой, то считываем элементы
        text = text_editor.get("1.0", END)  # Считываем данные с формы текста
        # Замена двойного переноса строки на один и пробела на запятую
        replacement = [['\n\n', '\n'], [' ', ';']]
        for old, new in replacement:
            text = text.replace(old, new)
        with open(filepath, "w") as file:  # Записываем данные в новый файл
            file.write(text)
    else:  # Если путь к файлу пустой, то вывод сообщения об ошибки
        mb.showerror(
            "Ошибка",
            "Путь для сохранения файла не выбран")


root = Tk()
root.title("geostatSGU")
root.attributes("-fullscreen", True)
open_button = Button(root, text="Открыть файл", font=40, command=open_file)
open_button.grid(column=0, row=0, padx=10, sticky=SE)

add_file_button = Button(root, text="Добавить файл", font=40, command=add_file, state='disabled')
add_file_button.grid(column=1, row=1, sticky=NW, padx=30, pady=(50, 0))

checkFlag = IntVar()
check_button = Checkbutton(root, text="Расчёт по градусам", variable=checkFlag, onvalue=1, offvalue=0)
check_button.grid(row=0, column=2, sticky=NE, pady=(30, 0), padx=30)

laplasian_button = Button(root, text="Посчитать лапласианы", font=40, command=calculate, state='disabled')
laplasian_button.grid(column=1, row=5, sticky=NW, padx=30, pady=(50, 0))
#
label_step1 = Label(root, text='Введите шаг широты:')
label_step1.grid(column=1, row=2, sticky=NW, padx=30)
entry1 = Entry(root)
entry1.grid(column=2, row=2, sticky=NE)
label_step2 = Label(root, text='Введите шаг долготы:')
label_step2.grid(column=1, row=3, sticky=NW, padx=30)
entry2 = Entry(root)
entry2.grid(column=2, row=3, sticky=NE)
send_button = Button(root, text="Отправить", font=40, command=send_steps)
send_button.grid(column=2, row=4, rowspan=2, sticky=NW)

text_editor = Text(height=30, width=90, font='11', undo=True)
scrollerY = Scrollbar(root, command=text_editor.yview)
scrollerX = Scrollbar(root, command=text_editor.xview, orient=HORIZONTAL)

text_editor.config(yscrollcommand=scrollerY.set, xscrollcommand=scrollerX.set, wrap=NONE)
text_editor.grid(column=0, rowspan=6, row=1, padx=10, sticky=NSEW)
scrollerY.grid(row=1, column=1, rowspan=6, sticky=['n', 's', 'w'])
scrollerX.grid(row=7, column=0, sticky=['e', 'n', 'w'])

save_buttonCSV = Button(text="Сохранить как CSV", command=save_fileCSV)
save_buttonCSV.grid(column=1, row=6, sticky=SW, padx=30, pady=(50, 0))

back_button = Button(root, text='Назад', command=lambda: text_editor.edit_undo())
back_button.grid(row=8, column=0, sticky=NW, padx=10)

mainmenu = Menu(root)
root.config(menu=mainmenu)
radio_state = IntVar()
radio_state.set(0)

filemenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Файл",
                     menu=filemenu)
filemenu.add_command(label="Открыть...", command=open_file)
formatmenu = Menu(filemenu, tearoff=0)
formatmenu.add_radiobutton(label='Fullscreen', variable=radio_state, command=changeFormat, value=0)
formatmenu.add_radiobutton(label='500x300', variable=radio_state, command=changeFormat, value=1)
filemenu.add_cascade(label="Формат", menu=formatmenu)
filemenu.add_command(label="Сохранить...", command=save_fileCSV)
filemenu.add_command(label="Завершить", command=lambda: root.quit())

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=func_help)
helpmenu.add_command(label="О программе", command=aboutProgram)
mainmenu.add_cascade(label="Справка",
                     menu=helpmenu)

root.mainloop()
