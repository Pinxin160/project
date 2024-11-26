# main.py
import tkinter as tk
from tkinter import messagebox
from user_manager import initialize_data, login, register

def login_screen():
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if login(username, password):
            messagebox.showinfo("成功", f"歡迎，{username}！")
            main_window.destroy()
        else:
            messagebox.showerror("錯誤", "帳號或密碼錯誤！")

    def switch_to_register():
        main_window.destroy()
        register_screen()

    main_window = tk.Tk()
    main_window.title("登入")
    tk.Label(main_window, text="帳號").grid(row=0, column=0)
    username_entry = tk.Entry(main_window)
    username_entry.grid(row=0, column=1)
    tk.Label(main_window, text="密碼").grid(row=1, column=0)
    password_entry = tk.Entry(main_window, show="*")
    password_entry.grid(row=1, column=1)
    tk.Button(main_window, text="登入", command=handle_login).grid(row=2, column=0, columnspan=2)
    tk.Button(main_window, text="註冊", command=switch_to_register).grid(row=3, column=0, columnspan=2)
    main_window.mainloop()

def register_screen():
    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        if register(username, password):
            messagebox.showinfo("成功", "註冊成功！請重新登入。")
            main_window.destroy()
            login_screen()
        else:
            messagebox.showerror("錯誤", "帳號已存在，請使用其他名稱！")

    def switch_to_login():
        main_window.destroy()
        login_screen()

    main_window = tk.Tk()
    main_window.title("註冊")
    tk.Label(main_window, text="帳號").grid(row=0, column=0)
    username_entry = tk.Entry(main_window)
    username_entry.grid(row=0, column=1)
    tk.Label(main_window, text="密碼").grid(row=1, column=0)
    password_entry = tk.Entry(main_window, show="*")
    password_entry.grid(row=1, column=1)
    tk.Button(main_window, text="註冊", command=handle_register).grid(row=2, column=0, columnspan=2)
    tk.Button(main_window, text="返回登入", command=switch_to_login).grid(row=3, column=0, columnspan=2)
    main_window.mainloop()

initialize_data()
login_screen()
