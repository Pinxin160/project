# user_manager.py
import json
import os

FILE_PATH = "users.json"

def initialize_data():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as file:
            json.dump({"users": []}, file)

def load_users():
    with open(FILE_PATH, 'r') as file:
        return json.load(file)

def save_users(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file)

def login(username, password):
    users = load_users()
    for user in users["users"]:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def register(username, password):
    users = load_users()
    if any(user["username"] == username for user in users["users"]):
        return False  # 帳號已存在
    users["users"].append({"username": username, "password": password, "level": 1})
    save_users(users)
    return True