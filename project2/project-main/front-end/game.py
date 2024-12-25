import tkinter as tk
from tkinter import messagebox

# 主視窗
main_window = tk.Tk()
main_window.title("遊戲選擇")

# 玩家資訊顯示
player_data = {"username": "player1", "level": 1, "score": 0}

def update_player_info():
    player_info_label.config(text=f"玩家名稱: {player_data['username']}\n等級: {player_data['level']}\n分數: {player_data['score']}")

player_info_label = tk.Label(main_window, font=("Arial", 12))
player_info_label.grid(row=0, column=0, padx=10, pady=5)
update_player_info()

# 遊戲選擇
def game_1():
    messagebox.showinfo("遊戲 1", "進入遊戲 1")
    main_window.withdraw()  # 隱藏主界面

def game_2():
    messagebox.showinfo("遊戲 2", "進入遊戲 2")
    main_window.withdraw()

def game_3():
    messagebox.showinfo("遊戲 3", "進入遊戲 3")
    main_window.withdraw()

# 遊戲選擇按鈕
tk.Button(main_window, text="遊戲 1", command=game_1).grid(row=1, column=0, padx=10, pady=5)
tk.Button(main_window, text="遊戲 2", command=game_2).grid(row=2, column=0, padx=10, pady=5)
tk.Button(main_window, text="遊戲 3", command=game_3).grid(row=3, column=0, padx=10, pady=5)

main_window.mainloop()