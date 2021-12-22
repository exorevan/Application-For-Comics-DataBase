import tkinter.ttk as ttk
import webbrowser
from tkinter import *

from config import *
from functions import *

current_cursor = 0
current_connection = 0
current_treeview = 0

current_table = ""


def menu():
    global root

    m = Menu(root)
    root.config(menu=m)

    fm = Menu(m)
    m.add_cascade(label="File...", menu=fm)
    fm.add_command(label="Выбрать БД", command=lambda: connect_window())
    # fm.add_command(label="Сохранить config")
    # fm.add_command(label="Сохранить таблицу как scv")
    # fm.add_command(label="Выход")

    rm = Menu(m)
    m.add_cascade(label="Pages", menu=rm)
    rm.add_command(label="Main menu", command=lambda: view())
    # rm.add_command(label="Добавление записи", command=lambda: add())


def add():
    global root

    root.destroy()
    root = Tk()
    menu()

    combo_tables = ttk.Combobox(root)
    combo_tables['values'] = ("countries", "persons", "publishers", "titles", "volumes", "professions", "posts")
    combo_tables.current(0)
    combo_tables.grid(column=0, row=0)


def view():
    global root

    root.destroy()
    root = Tk()
    root.title("Main menu")
    root.configure(background='#000080')
    root.wm_geometry("+%d+%d" % (700, 350))
    # root.geometry("1000x570")
    menu()

    label_greetings = Label(text="Welcome", font=('Comic Sans MS', 20), bg='#000080', fg='white')
    label_greetings.grid(row=0, column=0, columnspan=4)
    label_describe = Label(text="the biggest comics source", font=('Comic Sans MS', 14), bg='#000080', fg='white')
    label_describe.grid(row=1, column=0, columnspan=4, padx=5)
    label_traits = Label(text="——————————————————————————", font="Arial 14", bg='#000080', fg='white')
    label_traits.grid(row=2, column=0, columnspan=4, padx=5)
    label_categories = Label(text="Choose category:", font=('Comic Sans MS', 10), bg='#000080', fg='white')
    label_categories.grid(row=3, column=0, columnspan=4)

    button_publishers = Button(width=20, font=('Comic Sans MS', 10), bg='white', command=lambda: show_all_publishers())
    button_publishers["text"] = "Publishers"
    button_publishers.grid(column=0, row=4, columnspan=2, padx=10, pady=10)
    button_persons = Button(width=20, font=('Comic Sans MS', 10), bg='white', command=lambda: show_all_persons())
    button_persons["text"] = "Authors"
    button_persons.grid(column=2, row=4, columnspan=2, padx=10, pady=10)
    button_decades = Button(width=20, font=('Comic Sans MS', 10), bg='white', command=lambda: show_all_decades())
    button_decades["text"] = "Decades"
    button_decades.grid(column=0, row=5, columnspan=2, padx=10, pady=10)
    button_titles = Button(width=20, font=('Comic Sans MS', 10), bg='white', command=lambda: show_all_titles())
    button_titles["text"] = "Titles"
    button_titles.grid(column=2, row=5, columnspan=2, padx=10, pady=10)


def show_all_publishers():
    global root, current_treeview

    root.destroy()
    root = Tk()
    root.geometry("733x570+500+200")
    root.title("Publishers")
    menu()

    data = select_all("publishers", current_connection)

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20))
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12), background="silver", foreground="black", filedbackground="silver")
    # style_treeview.map('Treeview', background[('selected', 'green')])

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('ID', 'Name', 'Year found')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('ID', width=0, stretch=NO)
    current_treeview.column('Name', anchor=W, width=400)
    current_treeview.column('Year found', anchor=CENTER, width=333)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('ID', text='Id', anchor=CENTER)
    current_treeview.heading('Name', text='Name', anchor=CENTER)
    current_treeview.heading('Year found', text='Year found', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    current_treeview.bind('<Double-1>', select_from_publishers)
    current_treeview.grid(row=0, column=0)


def select_from_publishers(event, sort='name'):
    global root, current_treeview
    # data = select_publisher(current_treeview.get(current_treeview.curselection()), current_connection)
    # print(current_treeview.item(current_treeview.focus(), 'values'))
    selected = current_treeview.item(current_treeview.focus(), 'values')[1]
    data = select_publisher(selected, current_connection)

    # print(data)

    root.destroy()
    root = Tk()
    root.geometry("733x570+500+200")
    root.title("Titles from " + selected)
    menu()

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20))
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12))

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('ID', 'Name', 'Year start')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('ID', width=0, stretch=NO)
    current_treeview.column('Name', anchor=W, width=400)
    current_treeview.column('Year start', anchor=CENTER, width=333)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('ID', text='Id', anchor=CENTER)
    current_treeview.heading('Name', text='Name', anchor=CENTER)
    current_treeview.heading('Year start', text='Year start', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    current_treeview.bind('<Double-1>', select_from_titles)
    current_treeview.grid(row=0, column=0)


def select_from_titles(event):
    global root, current_treeview
    # data = select_publisher(current_treeview.get(current_treeview.curselection()), current_connection)
    # print(current_treeview.item(current_treeview.focus(), 'values'))
    selected = current_treeview.item(current_treeview.focus(), 'values')[1]
    data = select_volumes(selected, current_connection)

    # print(data)

    root.destroy()
    root = Tk()
    root.geometry("1130x570+500+200")
    root.title("Volumes of  " + selected)
    menu()

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20))
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12))

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('ID', 'Name', 'Year release', 'Publisher', 'Writer', 'Artist')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('ID', width=0, stretch=NO)
    current_treeview.column('Name', anchor=W, width=350)
    current_treeview.column('Year release', anchor=CENTER, width=200)
    current_treeview.column('Publisher', anchor=W, width=180)
    current_treeview.column('Writer', anchor=W, width=200)
    current_treeview.column('Artist', anchor=W, width=200)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('ID', text='Id', anchor=CENTER)
    current_treeview.heading('Name', text='Name', anchor=CENTER)
    current_treeview.heading('Year release', text='Year release', anchor=CENTER)
    current_treeview.heading('Publisher', text='Publisher', anchor=CENTER)
    current_treeview.heading('Writer', text='Writer', anchor=CENTER)
    current_treeview.heading('Artist', text='Artist', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    current_treeview.bind('<Double-1>', link_to_comics)
    current_treeview.grid(row=0, column=0)


def link_to_comics(event):
    global current_treeview

    # print(current_treeview.item(current_treeview.focus(), 'values')[1])
    search = current_treeview.item(current_treeview.focus(), 'values')[1]

    start = "https://drawnstories.ru/search/node/"
    end = search.replace(' ', '%20')

    webbrowser.open(str(start + end), new=1)


def show_all_persons():
    global root, current_treeview

    root.destroy()
    root = Tk()
    root.geometry("733x580+500+200")
    root.title("Persons")
    menu()

    data = select_all("persons", current_connection)

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20), fieldbackground="#120a8f", forebackground="#120a8f", background="#120a8f")
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12), fieldbackground="#120a8f", forebackground="#120a8f", background="#120a8f")

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('ID', 'Name', 'Year born')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('ID', width=0, stretch=NO)
    current_treeview.column('Name', anchor=W, width=400)
    current_treeview.column('Year born', anchor=CENTER, width=333)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('ID', text='Id', anchor=CENTER)
    current_treeview.heading('Name', text='Name', anchor=CENTER)
    current_treeview.heading('Year born', text='Year born', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    current_treeview.bind('<Double-1>', select_for_person)
    current_treeview.grid(row=0, column=0)


def select_for_person(event):
    global root, current_treeview

    selected = current_treeview.item(current_treeview.focus(), 'values')[1]
    data = select_author(selected, current_connection)
    # print(data)

    root.destroy()
    root = Tk()
    root.geometry("1110x570+500+200")
    root.title("Works of " + selected)
    menu()

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20))
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12))

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('Year', 'Volume', 'Title', 'Publisher', 'Post')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('Year', anchor=CENTER, width=100)
    current_treeview.column('Volume', anchor=W, width=360)
    current_treeview.column('Title', anchor=W, width=300)
    current_treeview.column('Publisher', anchor=W, width=200)
    current_treeview.column('Post', anchor=CENTER, width=150)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('Year', text='Year', anchor=CENTER)
    current_treeview.heading('Volume', text='Volume', anchor=CENTER)
    current_treeview.heading('Title', text='Title', anchor=CENTER)
    current_treeview.heading('Publisher', text='Publisher', anchor=CENTER)
    current_treeview.heading('Post', text='Post', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    current_treeview.bind('<Double-1>', link_to_comics)
    current_treeview.grid(row=0, column=0)


def show_all_decades():
    global root, current_treeview

    root.destroy()
    root = Tk()
    root.geometry("465x250+500+200")
    root.title("Decades")
    menu()

    label_check_decades = ttk.Label(text="Choose decade:", font="Arial 20")
    label_check_decades.grid(row=0, column=0, columnspan=4)

    but_40_50 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(1940))
    but_40_50["text"] = "1940-1950"
    but_40_50.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    but_50_60 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(1950))
    but_50_60["text"] = "1950-1960"
    but_50_60.grid(column=2, row=1, columnspan=2, padx=10, pady=10)

    but_60_70 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(1960))
    but_60_70["text"] = "1960-1970"
    but_60_70.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    but_70_80 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(1970))
    but_70_80["text"] = "1970-1980"
    but_70_80.grid(column=2, row=2, columnspan=2, padx=10, pady=10)

    but_80_90 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(1980))
    but_80_90["text"] = "1980-1990"
    but_80_90.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    but_90_00 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(1990))
    but_90_00["text"] = "1990-2000"
    but_90_00.grid(column=2, row=3, columnspan=2, padx=10, pady=10)

    but_00_10 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(2000))
    but_00_10["text"] = "2000-2010"
    but_00_10.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

    but_10_20 = Button(width=20, font=('Courier', 12), command=lambda: select_from_decades(2010))
    but_10_20["text"] = "2010-2020"
    but_10_20.grid(column=2, row=4, columnspan=2, padx=10, pady=10)


def select_from_decades(year):
    global root, current_treeview

    root.destroy()
    root = Tk()
    root.geometry("1210x570+500+200")
    root.title("Comics from " + str(year) + " to " + str(int(year) + int(10)))
    menu()

    data = select_decades(year, current_connection)

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20))
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12))

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('ID', 'Year', 'Name', 'Number', 'Title', 'Publisher')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('ID', width=0, stretch=NO)
    current_treeview.column('Year', anchor=CENTER, width=100)
    current_treeview.column('Name', anchor=W, width=380)
    current_treeview.column('Number', anchor=CENTER, width=150)
    current_treeview.column('Title', anchor=W, width=330)
    current_treeview.column('Publisher', anchor=W, width=250)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('ID', text='Id', anchor=CENTER)
    current_treeview.heading('Year', text='Year', anchor=CENTER)
    current_treeview.heading('Name', text='Name', anchor=CENTER)
    current_treeview.heading('Number', text='Volume №', anchor=CENTER)
    current_treeview.heading('Title', text='Title', anchor=CENTER)
    current_treeview.heading('Publisher', text='Publisher', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    # current_treeview.bind('<Double-1>', select_from_publishers)
    current_treeview.grid(row=0, column=0)


def show_all_titles():
    global root, current_treeview

    root.destroy()
    root = Tk()
    root.geometry("733x570+500+200")
    root.title("All titles")
    menu()

    data = select_all_titles(current_connection)

    style_treeview = ttk.Style()
    style_treeview.configure("Treeview.Heading", font=('Comic Sans MS', 20))
    style_treeview.configure("Treeview", font=('Comic Sans MS', 12))

    current_treeview = ttk.Treeview(height=27)

    current_treeview['columns'] = ('ID', 'Name', 'Publisher')

    current_treeview.column('#0', width=0, stretch=NO)
    current_treeview.column('ID', width=0, stretch=NO)
    current_treeview.column('Name', anchor=W, width=400)
    current_treeview.column('Publisher', anchor=W, width=333)

    current_treeview.heading('#0', text='', anchor=CENTER)
    current_treeview.heading('ID', text='Id', anchor=CENTER)
    current_treeview.heading('Name', text='Name', anchor=CENTER)
    current_treeview.heading('Publisher', text='Publisher', anchor=CENTER)

    for string in data:
        current_treeview.insert(parent='', index=END, text='', values=string)

    current_treeview.bind('<Double-1>', select_from_titles)
    current_treeview.grid(row=0, column=0)


def choose_config():
    pass


def connect_window():
    global root

    root.destroy()
    root = Tk()
    root.title("Connect")

    label_ip = ttk.Label(text="Введите хост IP: ", anchor=W, font="Courier 12", padding=(5, 5, 5, 5))
    label_ip.grid(column=0, row=1)
    ent_ip = Entry(font="Courier 12")
    ent_ip.grid(column=1, row=1, padx=5)

    label_port = ttk.Label(text="Введите порт: ", anchor=W, font="Courier 12", padding=(5, 5, 5, 5))
    label_port.grid(column=0, row=2)
    ent_port = Entry(font="Courier 12")
    ent_port.grid(column=1, row=2, padx=5)

    label_user = ttk.Label(text="Введите имя пользователя: ", anchor=W, font="Courier 12", padding=(5, 5, 5, 5))
    label_user.grid(column=0, row=3)
    ent_user = Entry(font="Courier 12")
    ent_user.grid(column=1, row=3)

    label_password = ttk.Label(text="Введите пароль: ", anchor=W, font="Courier 12", padding=(5, 5, 5, 5))
    label_password.grid(column=0, row=4)
    ent_password = Entry(font="Courier 12")
    ent_password.grid(column=1, row=4)

    label_db = ttk.Label(text="Введите имя БД: ", anchor=W, font="Courier 12", padding=(5, 5, 5, 5))
    label_db.grid(column=0, row=5)
    ent_db = Entry(font="Courier 12")
    ent_db.grid(column=1, row=5)

    but_choose_config = Button(width=25, command=lambda: choose_config())
    but_choose_config["text"] = "Выбрать конфиг"
    # but1.bind("<Button-1>", clean_frame)
    but_choose_config.grid(column=0, row=6, padx=10, pady=10)
    but_connect = Button(width=25,
                         command=lambda: connect(ent_ip.get(), ent_port.get(), ent_user.get(), ent_password.get(),
                                                 ent_db.get()))

    ent_ip.insert(0, host)
    ent_port.insert(0, port)
    ent_user.insert(0, user)
    ent_password.insert(0, password)
    ent_db.insert(0, db_name)

    but_connect["text"] = "Подключиться"
    # but1.bind("<Button-1>", clean_frame)
    but_connect.grid(column=1, row=6, padx=10, pady=10)


def connect(ip, port, user_name, password, db_name):
    global current_connection, root

    current_connection = connect_to_db(ip, user_name, password, db_name, port)

    if current_connection:
        view()


def choose_window(window_name):
    global root, style_treeview

    root = Tk()

    if window_name == "view":
        view()
    elif window_name == "connect":
        connect_window()

    root.mainloop()
