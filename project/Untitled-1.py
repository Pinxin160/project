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
def login():
    users = load_users()
    username = input("請輸入帳號: ")
    password = input("請輸入密碼: ")
    for user in users["users"]:
        if user["username"] == username and user["password"] == password:
            print(f"登入成功！歡迎，{username}")
            return user  # 回傳使用者資料
    print("帳號或密碼錯誤！")
    return None

# 註冊功能
def register():
    users = load_users()
    username = input("請創建帳號: ")
    if any(user["username"] == username for user in users["users"]):
        print("帳號已存在，請選擇其他名稱！")
        return
    password = input("請輸入密碼: ")
    new_user = {"username": username, "password": password, "level": 1}
    users["users"].append(new_user)
    save_users(users)
    print("註冊成功！")

# 主選單
def main_menu():
    initialize_data()
    while True:
        print("1. 登入")
        print("2. 註冊")
        print("3. 離開")
        choice = input("請選擇功能: ")
        if choice == "1":
            if login():
                break  # 成功登入後退出選單
        elif choice == "2":
            register()
        elif choice == "3":
            print("感謝使用，再見！")
            break
        else:
            print("無效選擇，請重新輸入。")

main_menu()