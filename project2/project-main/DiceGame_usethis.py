import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# 定義數字與符號的對應字典
DICE_SYMBOLS = {
    1: "⚀",
    2: "⚁",
    3: "⚂",
    4: "⚃",
    5: "⚄",
    6: "⚅"
}

# 玩家類別
class Player:
    def __init__(self, name):
        self.name = name
        self.dice = [random.randint(1, 6) for _ in range(5)]  # 初始化5顆骰子
        self.experience = 0  # 經驗值

    def roll_dice(self):
        self.dice = [random.randint(1, 6) for _ in range(len(self.dice))]  # 擲骰子

    def lose_dice(self):
        if self.dice:
            self.dice.pop()

    def add_experience(self, amount):
        self.experience += amount



# 遊戲主類別
class DiceGame:
    def show_number_pad(self):
        """顯示數字鍵盤讓玩家輸入報數。"""
        # 建立彈窗
        keypad_window = tk.Toplevel(self.root)
        keypad_window.title("數字鍵盤輸入報數")
        keypad_window.geometry("300x400")
        keypad_window.grab_set()  # 鎖定在彈窗內操作
    
        # 保存選擇的數量與數字
        selected_count = tk.IntVar(value=0)
        selected_value = tk.IntVar(value=0)
    
        # 更新顯示輸入的數量和數字
        def update_display():
            display_label.config(text=f"{selected_count.get()}個{selected_value.get() if selected_value.get() else ''}")
    
        # 清空輸入
        def clear_selection():
            selected_count.set(0)
            selected_value.set(0)
            update_display()
    
        # 確定輸入
        def confirm_selection():
            if selected_count.get() > 0 and selected_value.get() > 0:
                call = f"{selected_count.get()}個{selected_value.get()}"
                result = self.validate_call(call)
                if result:
                    self.previous_call = result
                    self.current_turn = "computer"
                    self.computer_turn()
                keypad_window.destroy()
            else:
                messagebox.showerror("錯誤", "請選擇數量和骰子的點數！")
    
        # 顯示目前輸入
        display_label = tk.Label(keypad_window, text="0個", font=("Helvetica", 20), relief="sunken", bg="white")
        display_label.pack(pady=10, fill=tk.X, padx=10)
    
        # 數量按鈕
        count_frame = tk.LabelFrame(keypad_window, text="數量", font=("Helvetica", 14))
        count_frame.pack(pady=10, fill=tk.X, padx=10)
    
        for i in range(1, 10):  # 假設數量最多為 9
            btn = tk.Button(count_frame, text=str(i), font=("Helvetica", 18),
                            command=lambda n=i: [selected_count.set(n), update_display()])
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
        # 骰子數值按鈕
        value_frame = tk.LabelFrame(keypad_window, text="骰子點數", font=("Helvetica", 14))
        value_frame.pack(pady=10, fill=tk.X, padx=10)
    
        for i in range(1, 7):  # 骰子數值為 1 到 6
            btn = tk.Button(value_frame, text=str(i), font=("Helvetica", 18),
                            command=lambda n=i: [selected_value.set(n), update_display()])
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
        # 控制按鈕
        control_frame = tk.Frame(keypad_window)
        control_frame.pack(pady=20)
    
        tk.Button(control_frame, text="清除", font=("Helvetica", 14), bg="white", fg="blueviolet", command=clear_selection).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="確定", font=("Helvetica", 14), bg="blueviolet", fg="white", command=confirm_selection).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="取消", font=("Helvetica", 14), bg="white", fg="blueviolet", command=keypad_window.destroy).pack(side=tk.LEFT, padx=10)

    def __init__(self, root):
        self.root = root
        self.root.title("🌬️🐮遊戲")

        # 遊戲狀態
        self.game_paused = False
        self.difficulty = None  # 預設電腦強度
        self.computer_loss_multiplier = 2  # 普通難度需打敗2次才減1顆骰子

        # 初始化玩家
        self.player = Player("玩家")
        self.computer = Player("電腦")
        self.all_players = [self.player, self.computer]

        # 初始化遊戲狀態
        self.previous_call = None
        self.current_turn = "player"
        self.computer_losses = 0

        # 建立 UI
        self.create_ui()

        # 綁定快捷鍵事件
        self.root.bind("<k>", self.toggle_pause)
        self.root.bind("<f>", self.quit_game)
        self.root.bind("<r>", self.restart_game)

    def create_ui(self):
        # 選擇電腦強度
        self.difficulty_label = tk.Label(self.root, text="選擇電腦強度：", font=("Helvetica", 14))
        self.difficulty_label.pack(pady=5)

        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack()

        tk.Button(self.difficulty_frame, text="🤷🏻‍👉", font=("Helvetica", 20), command=lambda: self.set_difficulty("easy"), width=10, bg="whitesmoke", fg="black").pack(side=tk.LEFT, padx=5)
        tk.Button(self.difficulty_frame, text="🙎‍👉", font=("Helvetica", 20), command=lambda: self.set_difficulty("normal"), width=10, bg="whitesmoke", fg="black").pack(side=tk.LEFT, padx=5)
        tk.Button(self.difficulty_frame, text="😈🪦", font=("Helvetica", 20), command=lambda: self.set_difficulty("hard"), width=10, bg="indigo", fg="white").pack(side=tk.LEFT, padx=5)

        # 開始遊戲按鈕
        self.start_button = tk.Button(self.root, text="開始遊戲", font=("Helvetica", 14), command=self.start_game, bg="gold", fg="red")
        self.start_button.pack(pady=20)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.computer_loss_multiplier = 1
            messagebox.showinfo("難度選擇", "easy peasy lemon squeezy~♫♩♪\n去選右邊的!!!!!!")
        elif difficulty == "normal":
            self.computer_loss_multiplier = 2
            messagebox.showinfo("難度選擇", "回去重選右邊的")
        elif difficulty == "hard":
            self.computer_loss_multiplier = 3
            messagebox.showinfo("難度選擇", "讓你體驗一下什麼是糞作game")

    def start_game(self):
        if not self.difficulty:  # 檢查是否已選擇難度
            messagebox.showerror("錯誤", "請先選擇遊戲難度！")
            return
        
        # 重置遊戲狀態
        self.player = Player("玩家")
        self.computer = Player("電腦")
        self.all_players = [self.player, self.computer]
        self.previous_call = None
        self.current_turn = "player"
        self.computer_losses = 0

        # 清除選擇難度與開始按鈕
        self.difficulty_label.pack_forget()
        self.difficulty_frame.pack_forget()
        self.start_button.pack_forget()

        # 創建遊戲 UI
        self.create_game_ui()

    # 修改 create_game_ui 方法
    def create_game_ui(self):
        # 玩家經驗值顯示
        self.experience_label = tk.Label(self.root, text=f"玩家經驗值：{self.player.experience}", font=("Helvetica", 14))
        self.experience_label.pack(pady=5)
    
        # 玩家資訊
        self.player_info = tk.Label(self.root, text="你的骰子：", font=("Helvetica", 14))
        self.player_info.pack()
    
        # 玩家骰子顯示
        self.dice_frame = tk.Frame(self.root)
        self.dice_frame.pack()
        self.player_dice_labels = [tk.Label(self.dice_frame, text=DICE_SYMBOLS[d], fg="mediumpurple", font=("Helvetica", 75)) for d in self.player.dice]
        for lbl in self.player_dice_labels:
            lbl.pack(side=tk.LEFT, padx=5)
    
        # 電腦骰子框架        
        self.computer_frame = tk.Label(self.root, text="電腦的骰子：", font=("Helvetica", 14))
        self.computer_frame.pack()
        self.computer_frame = tk.Frame(self.root)
        self.computer_frame.pack(pady=10)
        self.computer_labels = [tk.Label(self.computer_frame, text="🎲", fg="mediumpurple", font=("Helvetica", 50)) for _ in self.computer.dice]
        for lbl in self.computer_labels:
            lbl.pack(side=tk.LEFT, padx=5)
    
        # 顯示電腦報數
        self.computer_call_label = tk.Label(self.root, text="電腦報數：無", font=("Helvetica", 14))
        self.computer_call_label.pack(pady=5)
    
        # 動作按鈕
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)
    
        self.call_button = tk.Button(self.action_frame, text="報數", font=("Helvetica", 25), bg="white", fg="blueviolet", command=self.make_call)
        self.call_button.pack(side=tk.LEFT, padx=5)
    
        self.challenge_button = tk.Button(self.action_frame, text="抓🫵", font=("Helvetica", 25), bg="blueviolet", fg="white", command=self.challenge)
        self.challenge_button.pack(side=tk.LEFT, padx=5)
        
        # 重新開始按鈕
        self.restart_button = tk.Button(self.root, text="重新開始遊戲(R)", bg="whitesmoke", fg="mediumpurple", font=("Helvetica", 14), command=self.restart_game)
        self.restart_button.pack(pady=20)

    # 修改 update_ui 方法
    def update_ui(self):
        # 更新玩家經驗值
        self.experience_label.config(text=f"玩家經驗值：{self.player.experience}") 
        # 更新玩家骰子
        for i, lbl in enumerate(self.player_dice_labels):
            if i < len(self.player.dice):
                lbl.config(text=DICE_SYMBOLS[self.player.dice[i]])
            else:
                lbl.config(text="")
    
        # 更新電腦骰子問號數量
        for i, lbl in enumerate(self.computer_labels):
            if i < len(self.computer.dice):
                lbl.config(text="🎲")
            else:
                lbl.config(text="")


  
    def validate_call(self, call):
        try:
            count, value = map(int, call.split("個"))
            if value < 1 or value > 6 or count < len(self.all_players):
                raise ValueError("報數格式錯誤或不符合最小數量限制。")
            if self.previous_call:
                prev_count, prev_value = self.previous_call
                if count < prev_count or (count == prev_count and value <= prev_value):
                    raise ValueError("報數需比上一個報數更高。")
            return count, value
        except ValueError as e:
            messagebox.showerror("錯誤", str(e))
            return None

    def make_call(self):
        """玩家報數，使用數字鍵盤介面。"""
        self.show_number_pad()

                
    def computer_turn(self):
        total_dice = len(self.player.dice) + len(self.computer.dice)
        if random.random() < 0.3 or (self.previous_call and self.previous_call[0] > total_dice):
            self.challenge()
        else:
            if not self.previous_call:
                new_call = (len(self.all_players), random.randint(1, 6))
            else:
                count, value = self.previous_call
                if value < 6:
                    new_call = (count, value + 1)
                else:
                    new_call = (count + 1, 1)
            self.previous_call = new_call
            self.computer_call_label.config(text=f"電腦報數：{new_call[0]}個{new_call[1]}")
            self.current_turn = "player"
            
    def challenge(self):
        if not self.previous_call:
            messagebox.showerror("錯誤", "你還沒報數抓什麼抓🙄！")
            return
    
        count, value = self.previous_call
        actual_count = sum(1 for p in self.all_players for d in p.dice if d == value or d == 1)
    
        # 攤牌顯示
        result_text = f"場上骰子攤牌：\n玩家骰子：{self.player.dice}\n電腦骰子：{self.computer.dice}"
        result_text += f"\n場上共有 {actual_count} 顆 {value}（含萬能數字 1）。"
        messagebox.showinfo("攤牌結果", result_text)
    
        # 判定結果
        if actual_count >= count:
            if self.current_turn == "player":
                messagebox.showinfo("結果", "玩家抓錯了！")
                self.player.lose_dice()
            else:
                messagebox.showinfo("結果", "電腦抓錯了！")
                self.computer_losses += 1
                if self.computer_losses >= self.computer_loss_multiplier:
                    self.computer.lose_dice()
                    self.computer_losses = 0
                    self.player.add_experience(200)  # 增加經驗值
        else:
            if self.current_turn == "player":
                messagebox.showinfo("結果", "玩家抓對了！")
                self.computer_losses += 1
                if self.computer_losses >= self.computer_loss_multiplier:
                    self.computer.lose_dice()
                    self.computer_losses = 0
                    self.player.add_experience(200)  # 增加經驗值
            else:
                messagebox.showinfo("結果", "電腦抓對了！")
                self.player.lose_dice()
    
        # 玩家和電腦重新擲骰子
        self.player.roll_dice()
        self.computer.roll_dice()
    
        # 重置報數累積
        self.previous_call = None
        self.current_turn = "player"  # 揭穿結束後由玩家開始新一輪
        self.computer_call_label.config(text="電腦報數：無")
        
        self.update_ui()
        self.check_game_over()


    def check_game_over(self):
        if not self.player.dice:
            messagebox.showinfo("遊戲結束", "你輸了！🪦🪦🪦")
            self.restart_game()
        elif not self.computer.dice:
            messagebox.showinfo("遊戲結束", "你贏了！🎉🎉🎉")
            self.restart_game()
            self.player.add_experience(800)  # 增加經驗值

    def toggle_pause(self, event=None):
        self.game_paused = not self.game_paused
        if self.game_paused:
            messagebox.showinfo("遊戲暫停", "遊戲已暫停，按 'K' 以繼續遊戲。")
        else:
            messagebox.showinfo("遊戲繼續", "遊戲繼續進行！")

    def quit_game(self, event=None):
        if messagebox.askyesno("確認退出", "確定要退出遊戲嗎？"):
            self.root.destroy()

    def restart_game(self, event=None):
        if messagebox.askyesno("確認重啟", "確定要重啟遊戲嗎？"):
            self.root.destroy()
            root = tk.Tk()
            game = DiceGame(root)
            root.mainloop()

# 主程式
if __name__ == "__main__":
    root = tk.Tk()
    game = DiceGame(root)
    root.mainloop()
