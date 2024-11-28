import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from user_manager import initialize_data, login, register, load_users, save_users

def login_screen():

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if login(username, password):

            # 取得玩家資料
            users = load_users()
            current_user = next(user for user in users["users"] if user["username"] == username)

            messagebox.showinfo("成功", f"歡迎，{username}！")
            main_window.destroy()
            game_screen(current_user)
        else:
            messagebox.showerror("錯誤", "帳號或密碼錯誤！")

    def switch_to_register():
        main_window.destroy()
        register_screen()

    main_window = tk.Tk()
    main_window.title("登入")
    main_window.geometry("400x400")
    main_window.configure(bg="#f5f5f5")  # 更改背景顏色

    # 圖案
    image = Image.open("logo.png")
    image = image.resize((150, 150))
    logo = ImageTk.PhotoImage(image)  # 加載圖片
    tk.Label(main_window, image=logo, bg="#f5f5f5").grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(main_window, text="帳號", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    username_entry = tk.Entry(main_window, font=("Arial", 12))
    username_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(main_window, text="密碼", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(main_window, show="*", font=("Arial", 12))
    password_entry.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Button(main_window, text="登入", command=handle_login, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(main_window, text="註冊", command=switch_to_register, font=("Arial", 12)).grid(row=4, column=0, columnspan=2, pady=10)
    
    main_window.mainloop()


def register_screen():

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showinfo("失敗", "密碼與確認密碼不相符")
            return

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
    main_window.geometry("400x300")
    
    tk.Label(main_window, text="帳號", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(main_window, font=("Arial", 12))
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(main_window, text="密碼", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(main_window, show="*", font=("Arial", 12))
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(main_window, text="確認密碼", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
    confirm_password_entry = tk.Entry(main_window, show="*", font=("Arial", 12))
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Button(main_window, text="註冊", command=handle_register, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(main_window, text="返回登入", command=switch_to_login, font=("Arial", 12)).grid(row=4, column=0, columnspan=2, pady=10)
    
    main_window.mainloop()


def game_screen(current_user):

    def start_game(game_name):
        messagebox.showinfo("開始遊戲", f"{game_name} 開始！")
        # 根據遊戲名稱進行相應的遊戲邏輯處理

    def logout():
        main_window.destroy()
        login_screen()  # 登出後返回登入界面

    # 修改密碼
    def change_password():

        def handle_change_password():
            old_password = old_password_entry.get()
            new_password = new_password_entry.get()
            confirm_new_password = confirm_password_entry.get()

            if old_password != current_user['password']:
                messagebox.showerror("錯誤", "舊密碼錯誤！")
                return

            if new_password != confirm_new_password:
                messagebox.showerror("錯誤", "新密碼與確認密碼不相符！")
                return

            # 更新密碼
            users = load_users()
            for user in users["users"]:
                if user["username"] == current_user["username"]:
                    user["password"] = new_password
                    break
            save_users(users)

            messagebox.showinfo("成功", "密碼修改成功！")
            change_password_window.destroy()

        # 彈出修改密碼視窗
        change_password_window = tk.Toplevel(main_window)
        change_password_window.title("修改密碼")
        change_password_window.geometry("300x200")

        tk.Label(change_password_window, text="舊密碼", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        old_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 12))
        old_password_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(change_password_window, text="新密碼", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        new_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 12))
        new_password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(change_password_window, text="確認密碼", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
        confirm_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 12))
        confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(change_password_window, text="確認修改", command=handle_change_password, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=10)
    

    main_window = tk.Tk()
    main_window.title("遊戲選擇")
    main_window.geometry("400x400")
    main_window.configure(bg="#f5f5f5")

    # 顯示玩家資訊
    player_info_label = f"玩家名稱: {current_user['username']}\n等級: {current_user['level']}\n分數: {current_user['score']}"
    tk.Label(main_window, text=player_info_label, font=("Arial", 14), bg="#f5f5f5").grid(row=0, column=0, columnspan=2, pady=20)

    # 顯示遊戲選擇界面標題
    tk.Label(main_window, text="選擇一個遊戲", font=("Arial", 18)).grid(row=0, column=5, columnspan=2, pady=20)

    # 修改密碼按鈕
    tk.Button(main_window, text="修改密碼", command=change_password, font=("Arial", 12)).grid(row=1, column=8, columnspan=2, pady=10)

    # 遊戲選項按鈕
    tk.Button(main_window, text="遊戲一", command=lambda: start_game("遊戲一"), font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=10)
    tk.Button(main_window, text="遊戲二", command=lambda: start_game("遊戲二"), font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(main_window, text="遊戲三", command=lambda: start_game("遊戲三"), font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=10)
    
    # 登出按鈕
    tk.Button(main_window, text="登出", command=logout, font=("Arial", 12)).grid(row=4, column=0, columnspan=2, pady=10)

    main_window.mainloop()


initialize_data()
login_screen()
