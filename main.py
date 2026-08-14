from tkinter import Tk, PhotoImage, Menu, ttk, IntVar, Toplevel, messagebox, Text
from datetime import timedelta
import webbrowser
import subprocess
import re


def custom_window(name, title, dev=False):
    if hasattr(root, name) and getattr(root, name) is not None:
        getattr(root, name).lift()
        getattr(root, name).focus()
        return

    window = Toplevel(root)
    window.title(title)
    window.resizable(width=False, height=False)
    window.focus()

    if dev:
        ttk.Label(window, image=image).pack(padx=10, pady=10)
    else:
        txt = Text(window, relief="solid", font=("TkDefaultFont"), wrap="word", width=83, height=26)
        with open("LICENSE.txt", "r", encoding="UTF-8") as f:
            content = f.read()
        txt.insert("1.0", content)
        txt.config(state="disabled")
        txt.pack(padx=10, pady=10)

    def close_window():
        window.destroy()
        setattr(root, name, None)

    window.protocol("WM_DELETE_WINDOW", close_window)
    setattr(root, name, window)


def version():
    messagebox.showinfo(title="Версия", message="v3.2.1\n\n"
                                                "[ ! ] Упорядочено меню информации\n"
                                                "[ ! ] Прочие косметические улучшения")


def developer(x2dfox=False, git=False):
    if x2dfox:
        custom_window(name="image_window", title="x2DFox", dev=True)
    elif git:
        choice = messagebox.askyesno(title="GitHub", message="Перейти на страницу разработчика?")
        if choice:
            webbrowser.open("https://github.com/x2DFox")
    else:
        choice = messagebox.askyesno(title="Telegram", message="Перейти в канал разработчика?")
        if choice:
            webbrowser.open("https://t.me/x2DFox")


def license():
    custom_window(name="license_window", title="BSD 3-Clause License")


def change(*args):
    hour_label["text"] = f"Часы: {hour.get()}"
    minute_label["text"] = f"Минуты: {minute.get()}"


def enable(preset=None):
    if preset is None:
        preset = (int(hour.get())*3600 + int(minute.get())*60)
        if not preset:
            messagebox.showerror(title="Ошибка", message="Время не настроено")
            return
        for var in [hour, minute]:
            var.set(0)
        change(None)

    command = subprocess.run(["shutdown", "/s", "/t", f"{preset}"], capture_output=True, text=True)
    if re.search("1190", command.stderr):
        messagebox.showerror(title="Ошибка", message="Таймер уже активирован")
    else:
        messagebox.showinfo(title="Успех", message=f"{'Компьютер выключится через'} {timedelta(seconds=preset)}")


def disable():
    command = subprocess.run(["shutdown", "/a"], capture_output=True, text=True)
    if re.search("1116", command.stderr):
        messagebox.showerror(title="Ошибка", message="Таймер не активирован")
    else:
        messagebox.showinfo(title="Успех", message="Таймер деактивирован")


root = Tk()
root.title("Shutdown Timer")
icon = PhotoImage(file="resources/16x16.png")
root.iconphoto(True, icon)
root.geometry("350x230")
root.resizable(width=False, height=False)

main_menu = Menu(tearoff=0)
file_menu = Menu(tearoff=0)
developer_menu = Menu(tearoff=0)

file_menu.add_command(label="Версия", command=version)
file_menu.add_cascade(label="Разработчик", menu=developer_menu)
file_menu.add_command(label="Лицензия", command=license)

developer_menu.add_cascade(label="x2DFox", command=lambda: developer(x2dfox=True))
image = PhotoImage(file="resources/developer.png")
developer_menu.add_cascade(label="GitHub", command=lambda: developer(git=True))
developer_menu.add_cascade(label="Telegram", command=lambda: developer())

main_menu.add_cascade(label="Информация", menu=file_menu)
root.config(menu=main_menu)

ttk.Frame(relief="solid").place(x=10, y=20, width=330, height=80)
ttk.Label(text="Быстрый старт").place(x=135, y=10)
ttk.Button(text="0:30", command=lambda: enable(1800)).place(x=20, y=30, width=70, height=25)
ttk.Button(text="1:00", command=lambda: enable(3600)).place(x=100, y=30, width=70, height=25)
ttk.Button(text="1:30", command=lambda: enable(5400)).place(x=180, y=30, width=70, height=25)
ttk.Button(text="2:00", command=lambda: enable(7200)).place(x=260, y=30, width=70, height=25)
ttk.Button(text="2:30", command=lambda: enable(9000)).place(x=20, y=65, width=70, height=25)
ttk.Button(text="3:00", command=lambda: enable(10800)).place(x=100, y=65, width=70, height=25)
ttk.Button(text="3:30", command=lambda: enable(12600)).place(x=180, y=65, width=70, height=25)
ttk.Button(text="4:00", command=lambda: enable(14400)).place(x=260, y=65, width=70, height=25)

hour = IntVar(value=0)
hour_label = ttk.Label(text=f"Часы: {hour.get()}")
hour_label.place(x=10, y=110)
ttk.Scale(from_=0, to=23, orient="horizontal", variable=hour, command=change, length=160).place(x=10, y=130)

minute = IntVar(value=0)
minute_label = ttk.Label(text=f"Минуты: {minute.get()}")
minute_label.place(x=180, y=110)
ttk.Scale(from_=0, to=59, orient="horizontal", variable=minute, command=change, length=160).place(x=180, y=130)

ttk.Button(text="АКТИВИРОВАТЬ", command=enable).place(x=10, y=165, width=330)
ttk.Button(text="ДЕАКТИВИРОВАТЬ", command=disable).place(x=10, y=195, width=330)

root.mainloop()
