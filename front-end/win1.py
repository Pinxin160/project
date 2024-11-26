import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_PATH = "users.json"

# 初始化使用者資料
def initialize_data():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as file:
            json.dump({"users": []}, file)

# 讀取使用者資料
def load_users():
    with open(FILE_PATH, 'r') as file:
        return json.load(file)

# 儲存使用者資料
def save_users(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file)

# 登入功能
def login(username, password):
    users = load_users()
    for user in users["users"]:
        if user["username"] == username and user["password"] == password:
            return True
    return False

# 註冊功能
def register(username, password):
    users = load_users()
    if any(user["username"] == username for user in users["users"]):
        return False  # 帳號已存在
    users["users"].append({"username": username, "password": password, "level": 1})
    save_users(users)
    return True

# 登入介面
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

# 註冊介面
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

# 初始化檔案並啟動程式
initialize_data()
login_screen()