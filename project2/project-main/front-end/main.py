import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from user_manager import initialize_data, login, register, load_users, save_users


def toggle_password_visibility(password_entry, toggle_button):
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_button.config(text="隱藏")
    else:
        password_entry.config(show='*')
        toggle_button.config(text="顯示")

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

    def switch_to_forgot_password():
        # 這是進入忘記密碼的頁面
        main_window.destroy()
        forgot_password_screen()

    main_window = tk.Tk()
    main_window.title("登入")
    main_window.geometry("1280x720")  # 調整視窗大小

    # 加載背景圖片
    bg_image = Image.open("background1.jpg")  # 確保圖片路徑正確
    bg_image = bg_image.resize((1280, 720))  # 調整背景大小適應視窗
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(main_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # 設定背景圖片填滿整個視窗

    # 創建普通矩形框架的函數 (使用Canvas)
    def create_rectangle_frame(parent, width, height, color="white"):
        canvas = tk.Canvas(parent, width=width, height=height, bd=0, highlightthickness=1)
        canvas.place(x=470, y=300)

        # 使用 create_rectangle 繪製矩形
        canvas.create_rectangle(0, 0, width, height, fill=color, outline="gray", width=2)

        return canvas

    # 使用創建矩形框架的函數
    input_frame = create_rectangle_frame(main_window, width=450, height=300, color="#f0f0f0")

    # 帳號輸入框
    tk.Label(input_frame, text=" 帳號 ", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, pady=5)
    username_entry = tk.Entry(input_frame, font=("Arial", 12), bd=1, relief="solid", width=18)
    username_entry.grid(row=0, column=1, pady=5, sticky="ew")

    # 密碼輸入框
    tk.Label(input_frame, text=" 密碼 ", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=1, column=0, pady=5)
    password_entry = tk.Entry(input_frame, show="*", font=("Arial", 12), bd=1, relief="solid", width=18)
    password_entry.grid(row=1, column=1, pady=5, sticky="ew")

    # 密碼顯示/隱藏按鈕
    toggle_button = tk.Button(input_frame, text="顯示", command=lambda: toggle_password_visibility(password_entry, toggle_button),
                            font=("Arial", 9, "bold"), bg="#ffcc00", fg="white", relief="flat", width=6, height=1)
    toggle_button.grid(row=1, column=2, padx=5, pady=5)

    # 登入按鈕
    login_button = tk.Button(input_frame, text="登入", command=handle_login, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", height=1, relief="raised", width=6)
    login_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # 註冊按鈕
    register_button = tk.Button(input_frame, text="註冊", command=switch_to_register, font=("Arial", 12, "bold"), bg="#008CBA", fg="white", height=1, relief="raised", width=6)
    register_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    # 忘記密碼按鈕
    forgot_password_button = tk.Button(input_frame, text="忘記密碼?", command=switch_to_forgot_password, font=("Arial", 9, "bold"), bg="#ff6347", fg="white", relief="flat")
    forgot_password_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # 顯示視窗
    main_window.mainloop()

def forgot_password_screen():
    def validate_security_answer():
        username = username_entry.get()
        answer = answer_entry.get()
        users = load_users()

        # 驗證安全問題
        for user in users["users"]:
            if user["username"] == username:
                if user["security_answer"] == answer:
                    messagebox.showinfo("成功", f"您的密碼為：{user['password']}")
                    forgot_window.destroy()
                    login_screen()
                    return
                else:
                    messagebox.showerror("錯誤", "答案錯誤！")
                    return

        messagebox.showerror("錯誤", "找不到該帳號！")

    def switch_to_login():
        forgot_window.destroy()
        login_screen()

    def show_security_question():
        username = username_entry.get()
        users = load_users()
        for user in users["users"]:
            if user["username"] == username:
                question_label.config(text=f"安全問題：{user['security_question']}")
                return
        question_label.config(text="找不到該帳號！")

    forgot_window = tk.Tk()
    forgot_window.title("忘記密碼")
    forgot_window.geometry("400x500")
    forgot_window.config(bg="#f0f8ff")  # 背景顏色

    # 標題
    tk.Label(forgot_window, text="忘記密碼", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#333").pack(pady=20)

    # 輸入帳號
    tk.Label(forgot_window, text="請輸入您的帳號", font=("Arial", 14), bg="#f0f8ff", fg="#333").pack(pady=5)
    username_entry = tk.Entry(forgot_window, font=("Arial", 14), width=30, bd=2, relief="solid")
    username_entry.pack(pady=5)

    # 確認帳號按鈕
    check_button = tk.Button(
        forgot_window,
        text="確認帳號",
        command=show_security_question,
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        relief="raised",
        bd=3,
        width=20
    )
    check_button.pack(pady=10)

    # 顯示安全問題
    question_label = tk.Label(
        forgot_window,
        text="安全問題：",
        font=("Arial", 12, "italic"),
        bg="#e6f7ff",
        fg="#00509e",
        wraplength=300,
        width=30,
        relief="groove",
        bd=2,
        height=3
    )
    question_label.pack(pady=10)

    # 輸入答案
    tk.Label(forgot_window, text="請輸入您的答案", font=("Arial", 14), bg="#f0f8ff", fg="#333").pack(pady=5)
    answer_entry = tk.Entry(forgot_window, font=("Arial", 14), width=30, bd=2, relief="solid")
    answer_entry.pack(pady=5)

    # 確認答案按鈕
    validate_button = tk.Button(
        forgot_window,
        text="驗證答案",
        command=validate_security_answer,
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        relief="raised",
        bd=3,
        width=20
    )
    validate_button.pack(pady=10)

    # 返回登入按鈕
    back_button = tk.Button(
        forgot_window,
        text="返回登入",
        command=switch_to_login,
        font=("Arial", 12),
        bg="#ff6347",
        fg="white",
        relief="raised",
        bd=3,
        width=20
    )
    back_button.pack(pady=10)

    forgot_window.mainloop()


def register_screen():
    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        security_question = question_entry.get()
        security_answer = answer_entry.get()

        if password != confirm_password:
            messagebox.showinfo("失敗", "密碼與確認密碼不相符")
            return

        if not username or not password or not security_question or not security_answer:
            messagebox.showerror("失敗", "所有欄位都必須填寫！")
            return

        if register(username, password, security_question, security_answer):
            messagebox.showinfo("成功", "註冊成功！請重新登入。")
            main_window.destroy()
            login_screen()
        else:
            messagebox.showerror("失敗", "帳號已存在，請使用其他名稱！")

    def switch_to_login():
        main_window.destroy()
        login_screen()

    def toggle_password_visibility(entry, button):
        if entry.cget('show') == '*':
            entry.config(show='')
            button.config(text='隱藏')
        else:
            entry.config(show='*')
            button.config(text='顯示')

    # 主視窗設置
    main_window = tk.Tk()
    main_window.title("註冊")
    main_window.geometry("400x350")
    main_window.configure(bg="#f0f8ff")

    # 標題
    tk.Label(
        main_window,
        text="註冊新帳號",
        font=("Arial", 20, "bold"),
        fg="#333",
        bg="#f0f8ff"
    ).grid(row=0, column=1, columnspan=1, pady=15)

    # 帳號欄位
    tk.Label(main_window, text="帳號", font=("Arial", 14), bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(main_window, font=("Arial", 12), width=20, bd=2, relief="solid")
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    # 密碼欄位
    tk.Label(main_window, text="密碼", font=("Arial", 14), bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(main_window, show="*", font=("Arial", 12), width=20, bd=2, relief="solid")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

   # 密碼顯示/隱藏按鈕
    toggle_button = tk.Button(
        main_window,
        text="顯示",
        command=lambda: toggle_password_visibility(password_entry, toggle_button),
        font=("Arial", 9, "bold"),
        bg="#ffcc00",
        fg="white",
        relief="ridge",
        width=5,
        height=0
    )
    toggle_button.grid(row=2, column=2, padx=5, pady=5)

    # 確認密碼欄位
    tk.Label(main_window, text=" 確認密碼", font=("Arial", 14), bg="#f0f8ff").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    confirm_password_entry = tk.Entry(main_window, show="*", font=("Arial", 12), width=20, bd=2, relief="solid")
    confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

    # 確認密碼顯示/隱藏按鈕
    confirm_toggle_button = tk.Button(
        main_window,
        text="顯示",
        command=lambda: toggle_password_visibility(confirm_password_entry, confirm_toggle_button),
        font=("Arial", 9, "bold"),
        bg="#ffcc00",
        fg="white",
        relief="ridge",
        width=5,
        height=0
    )
    confirm_toggle_button.grid(row=3, column=2, padx=5, pady=5)

    # 安全問題欄位
    tk.Label(main_window, text=" 安全問題", font=("Arial", 14), bg="#f0f8ff").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    question_entry = tk.Entry(main_window, font=("Arial", 12), width=20, bd=2, relief="solid")
    question_entry.grid(row=4, column=1, padx=10, pady=5)

    # 答案欄位
    tk.Label(main_window, text="答案", font=("Arial", 14), bg="#f0f8ff").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    answer_entry = tk.Entry(main_window, font=("Arial", 12), width=20, bd=2, relief="solid")
    answer_entry.grid(row=5, column=1, padx=10, pady=5)

    # 調整按鈕的行
    # 註冊按鈕和返回登入按鈕的容器
    button_frame = tk.Frame(main_window, bg="#f0f8ff")  # 使用 Frame 容器
    button_frame.grid(row=6, column=1, columnspan=1, pady=25)

    # 註冊按鈕
    tk.Button(
        button_frame,
        text="註冊",
        command=handle_register,
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        relief="raised",
        width=9,
        height=1
    ).grid(row=0, column=0, padx=(20, 10), sticky="w")  # 左對齊

    # 返回登入按鈕
    tk.Button(
        button_frame,
        text="返回登入",
        command=switch_to_login,
        font=("Arial", 10, "bold"),
        bg="#ff6347",
        fg="white",
        relief="raised",
        width=9,
        height=1
    ).grid(row=0, column=1, padx=(10, 20), sticky="e")  # 右對齊

    main_window.mainloop()

import chess_game_encrypted, DiceGame, os ,貪食蛇_加入排行榜

def game_screen(current_user):

    def start_game(game_name):
        messagebox.showinfo("開始遊戲", f"{game_name} 開始！")
        # 根據遊戲名稱進行相應的遊戲邏輯處理
        user_account = current_user

        if game_name == "象棋":
            folder_path = "./chess_game_records"
            file_name = f"{str(user_account)}.encrypted"    
            print("current before",current_user["score"])
            if file_name in os.listdir(folder_path): # 找目前這個使用者是否有上一次的象棋遊戲紀錄
                saved_last_game = folder_path + "/" + file_name
                print(f"檔案 {file_name} 存在於資料夾 {folder_path} 中。")
            else:
                saved_last_game = None
                print(f"檔案 {file_name} 不存在於資料夾 {folder_path} 中。")

            chess_game_encrypted.main(user_account, saved_last_game)
            print("current",current_user["score"])
        
        elif game_name == "吹牛":
            game = DiceGame
            exp = game.run(user_account)
            print("OVER")
            #exp = game.DiceGame.get_exp()
            #print("exp",exp)
        elif game_name == "貪食蛇":
            player_name = current_user['username']
            貪食蛇_加入排行榜.get_player_name(player_name)
            貪食蛇_加入排行榜.main()

        
        update_score(exp)

    def update_score(score):
        current_user['score'] += score
        if current_user['score'] >= 2**(current_user['level'] - 1) * 1000:
            current_user['level'] += 1
            current_user['score'] = 0  # 升級後分數歸零
            current_user['score'] = current_user['score'] + score
            if current_user['score'] == 2^(current_user['level']-1)*1000:
                current_user['level'] = current_user['level'] +1
                current_user['score'] = 0
        player_info_label = f"玩家名稱: {current_user['username']}\n等級: {current_user['level']}\n分數: {current_user['score']}"
        tk.Label(main_window, text=player_info_label, font=("Arial", 14), bg="#f5f5f5", anchor="w").grid(row=0, column=0, columnspan=2, padx=20, pady=20)

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
        change_password_window.geometry("400x250")
        change_password_window.configure(bg="#f0f8ff")  # 淡藍色背景

        # 標籤與輸入框
        tk.Label(change_password_window, text="舊密碼", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        old_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 12))
        old_password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(change_password_window, text="新密碼", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        new_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 12))
        new_password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(change_password_window, text="確認密碼", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        confirm_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 12))
        confirm_password_entry.grid(row=3, column=1, padx=10, pady=10)

        # 顯示密碼功能
        toggle_button1 = tk.Button(change_password_window, text="顯示", command=lambda: toggle_password_visibility(old_password_entry, toggle_button1))
        toggle_button1.grid(row=1, column=2, padx=5, pady=5)

        toggle_button2 = tk.Button(change_password_window, text="顯示", command=lambda: toggle_password_visibility(new_password_entry, toggle_button2))
        toggle_button2.grid(row=2, column=2, padx=5, pady=5)

        toggle_button3 = tk.Button(change_password_window, text="顯示", command=lambda: toggle_password_visibility(confirm_password_entry, toggle_button3))
        toggle_button3.grid(row=3, column=2, padx=5, pady=5)

        # 確認修改密碼按鈕
        tk.Button(change_password_window, text="確認修改", command=handle_change_password, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=3, pady=20)

    main_window = tk.Tk()
    main_window.title("遊戲選擇")
    main_window.geometry("500x500")

    # 加載背景圖片
    bg_image = Image.open("background2.jpg")  # 確保圖片路徑正確
    bg_image = bg_image.resize((500, 500))  # 調整背景大小適應視窗
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(main_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # 設定背景圖片填滿整個視窗

    # 顯示玩家資訊
    player_info_label = f"玩家名稱: {current_user['username']}\n等級: {current_user['level']}\n分數: {current_user['score']}"
    tk.Label(main_window, text=player_info_label, font=("Arial", 14), bg="#f5f5f5", anchor="w").grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    # 顯示遊戲選擇界面標題
    tk.Label(main_window, text="選擇一個遊戲", font=("Arial", 18, "bold"), bg="#f5f5f5").grid(row=1, column=0, columnspan=2, pady=20)

    # 修改密碼按鈕
    tk.Button(main_window, text="修改密碼", command=change_password, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    # 遊戲選項按鈕
    tk.Button(main_window, text="貪食蛇", command=lambda: start_game("貪食蛇"), font=("Arial", 12), bg="#2196F3", fg="white").grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(main_window, text="象棋", command=lambda: start_game("象棋"), font=("Arial", 12), bg="#2196F3", fg="white").grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(main_window, text="吹牛", command=lambda: start_game("吹牛"), font=("Arial", 12), bg="#2196F3", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

    # 登出按鈕
    tk.Button(main_window, text="登出", command=logout, font=("Arial", 12), bg="#ff6347", fg="white").grid(row=6, column=0, columnspan=2, pady=20)

    main_window.mainloop()

initialize_data()
login_screen()