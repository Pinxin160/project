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
        """顯示數字鍵盤讓玩家輸入報數"""
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
            display_label.config(text=f"{selected_count.get()}\u500b{selected_value.get() if selected_value.get() else ''}")

        # 清空輸入
        def clear_selection():
            selected_count.set(0)
            selected_value.set(0)
            update_display()

        # 確定輸入
        def confirm_selection():
            if selected_count.get() > 0 and selected_value.get() > 0:
                call = (selected_count.get(), selected_value.get())
                if not self.previous_call or (call[0] > self.previous_call[0] or (call[0] == self.previous_call[0] and call[1] > self.previous_call[1])):
                    self.previous_call = call
                    self.current_turn = "computer"
                    self.computer_turn()
                    keypad_window.destroy()
                else:
                    messagebox.showerror("\u932f\u8aa4", "\u5831\u6578\u5fc5\u9808\u9ad8\u65bc\u4e0a\u4e00\u500b\u5831\u6578\uff01")
            else:
                messagebox.showerror("\u932f\u8aa4", "\u8acb\u9078\u64c7\u6578\u91cf\u548c\u9ab0\u5b50\u7684\u9ede\u6578\uff01")

        # 顯示目前輸入
        display_label = tk.Label(keypad_window, text="0\u500b", font=("Helvetica", 20), relief="sunken", bg="white")
        display_label.pack(pady=10, fill=tk.X, padx=10)

        # 數量按鈕
        count_frame = tk.LabelFrame(keypad_window, text="\u6578\u91cf", font=("Helvetica", 14))
        count_frame.pack(pady=10, fill=tk.X, padx=10)

        for i in range(1, 11):  # 假設數量最多為 9
            btn = tk.Button(count_frame, text=str(i), font=("Helvetica", 18),
                            command=lambda n=i: [selected_count.set(n), update_display()])
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # 骰子數值按鈕
        value_frame = tk.LabelFrame(keypad_window, text="\u9ab0\u5b50\u9ede\u6578", font=("Helvetica", 14))
        value_frame.pack(pady=10, fill=tk.X, padx=10)

        for i in range(1, 7):  # 骰子數值為 1 到 6
            btn = tk.Button(value_frame, text=str(i), font=("Helvetica", 18),
                            command=lambda n=i: [selected_value.set(n), update_display()])
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # 控制按鈕
        control_frame = tk.Frame(keypad_window)
        control_frame.pack(pady=20)

        tk.Button(control_frame, text="\u6e05\u9664", font=("Helvetica", 14), bg="white", fg="blueviolet", command=clear_selection).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="\u78ba\u5b9a", font=("Helvetica", 14), bg="blueviolet", fg="white", command=confirm_selection).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="\u53d6\u6d88", font=("Helvetica", 14), bg="white", fg="blueviolet", command=keypad_window.destroy).pack(side=tk.LEFT, padx=10)


    def __init__(self, root, user_account):
        self.root = root
        self.root.title("🌬️🐮遊戲")

        # 遊戲狀態
        self.game_paused = False
        self.difficulty = None  # 預設電腦強度
        self.computer_loss_multiplier = 1  # 普通難度需打敗2次才減1顆骰子

        # 初始化玩家
        self.user_account = user_account
        self.user_account_id = user_account['username']
        self.original_score = user_account['score']  # 記錄玩家登入時的分數
        self.user_account_score = user_account['score']
        self.player = Player(self.user_account_id)
        self.computer = Player("電腦")
        self.all_players = [self.player, self.computer]
        
        # 初始化遊戲狀態
        self.previous_call = None
        self.current_turn = "player"
        self.computer_losses = 0
        self.score = 0
        # 建立 UI
        self.create_ui()

        # 綁定快捷鍵事件
        self.root.bind("<k>", self.toggle_pause)
        self.root.bind("<f>", self.quit_game)
        self.root.bind("<r>", self.restart_game)

    def create_ui(self):
        # 選擇電腦強度
        self.difficulty_frame = tk.Frame(self.root)  # 用來容納難度選擇畫面
        self.difficulty_frame.pack(fill=tk.BOTH, expand=True)
        
        self.difficulty_label = tk.Label(self.root, text="選擇電腦強度：", font=("Helvetica", 14))
        self.difficulty_label.pack(pady=5)

        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack()

        tk.Button(self.difficulty_frame, text="🤷🏻‍👉", font=("Helvetica", 20), command=lambda: self.set_difficulty("easy"), width=10, bg="whitesmoke", fg="black").pack(side=tk.LEFT, padx=5)
        tk.Button(self.difficulty_frame, text="😈🪦", font=("Helvetica", 20), command=lambda: self.set_difficulty("hard"), width=10, bg="indigo", fg="white").pack(side=tk.LEFT, padx=5)

        # 開始遊戲按鈕
        self.start_button = tk.Button(self.root, text="開始遊戲", font=("Helvetica", 14), command=self.start_game, bg="gold", fg="red")
        self.start_button.pack(pady=20)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.computer_loss_multiplier = 1
            messagebox.showinfo("難度選擇", "簡單模式已選擇！")
        elif difficulty == "hard":
            self.computer_loss_multiplier = 3
            messagebox.showinfo("難度選擇", "困難模式已選擇！")

    def start_game(self):
        if not self.difficulty:  # 檢查是否已選擇難度
            messagebox.showerror("錯誤", "請先選擇遊戲難度！")
            return
        
        # 隱藏難度選擇
        self.difficulty_frame.pack_forget()
        # 重置遊戲狀態
        self.player = Player(self.user_account_id)
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
        """電腦的回合：依據難度選擇行動邏輯"""
        total_dice = len(self.player.dice) + len(self.computer.dice)
    
        if self.difficulty == "easy":
            self.easy_computer_turn(total_dice)
        elif self.difficulty == "hard":
            self.hard_computer_turn(total_dice)
    
    def easy_computer_turn(self, total_dice):
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



    def hard_computer_turn(self, total_dice):
        """困難模式的電腦邏輯，加入統計和概率推測"""
        computer_dice = self.computer.dice
        
        # 計算電腦自己的骰子點數
        dice_counts = {i: computer_dice.count(i) for i in range(1, 7)}
        wildcard_count = dice_counts[1]  # 萬能骰子
        
        # 記錄過去的骰子頻率，用來估算未來的點數分布
        past_dice_rolls = self.get_past_dice_rolls()  # 假設有一個方法記錄所有過去的骰子結果
        past_counts = {i: past_dice_rolls.count(i) for i in range(1, 7)}
        
        # 根據過去的頻率來調整對玩家的估算
        estimated_player_counts = total_dice - len(computer_dice)
        adjusted_estimated_counts = {
            i: estimated_player_counts * (past_counts.get(i, 0) + 1) / (sum(past_counts.values()) + 6)  # 給予每個數字的概率調整
            for i in range(2, 7)
        }
        
        # 考慮萬能骰子對估算的影響，對每個數字進行加權
        adjusted_estimated_counts = {
            i: adjusted_estimated_counts.get(i, 0) + wildcard_count / 6
            for i in range(2, 7)
        }
        
        # 計算每個數字的可能最大數量（自己的點數 + 假設對方的點數）
        max_possible = {
            i: dice_counts.get(i, 0) + wildcard_count + adjusted_estimated_counts.get(i, 0)
            for i in range(2, 7)
        }
        
        # 如果是第一輪報數
        if not self.previous_call:
            # 根據頻率選擇電腦自己最多的點數進行報數
            confident_value = max(dice_counts, key=lambda x: dice_counts[x] if x > 1 else 0)
            new_call = (1, confident_value)  # 從 1 個該點數開始
        else:
            # 處理非第一輪的報數邏輯
            previous_count, previous_value = self.previous_call
        
            # 如果上一輪的報數不合理，選擇挑戰
            if max_possible.get(previous_value, 0) < previous_count:
                self.challenge()
                return
            
            # 決定跳號或逐步增加
            best_value = max(max_possible, key=lambda x: max_possible[x])
        
            # 如果最大可能數量遠高於上一輪，嘗試跳號
            if max_possible[best_value] > previous_count + 2:
                new_call = (previous_count + 2, best_value)  # 跳號報數
            else:
                # 若無法跳號，根據邏輯逐步增加數量或更換點數
                if previous_value < best_value:
                    new_call = (previous_count, best_value)  # 提升點數
                else:
                    new_call = (previous_count + 1, previous_value)  # 增加數量
        
        # 更新報數並顯示
        self.previous_call = new_call
        self.computer_call_label.config(
            text=f"電腦報數：{new_call[0]}個{new_call[1]}"
        )
        self.current_turn = "player"
    
    def get_past_dice_rolls(self):
        """返回過去所有骰子的點數"""
        # 假設這個方法能從遊戲狀態中取出所有骰子的結果，包括玩家和電腦的
        return self.computer.dice + self.player.dice  # 假設有player屬性

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
                    if not self.player.dice:  # 檢查玩家是否還有骰子
                        self.check_game_over()
                        return
                    self.player.add_experience(200)  # 增加經驗值
                  #  self.user_account['score'] += 200  # 累計分數
                  #  self.user_account['score'] += self.score
        else:
            if self.current_turn == "player":
                messagebox.showinfo("結果", "玩家抓對了！")
                self.computer_losses += 1
                if self.computer_losses >= self.computer_loss_multiplier:
                    self.computer.lose_dice()
                    self.computer_losses = 0
                    if not self.computer.dice:  # 檢查電腦是否還有骰子
                        self.check_game_over()
                        return
                    self.player.add_experience(200)  # 增加經驗值
                  #  self.user_account['score'] += 200  # 累計分數
                  #  self.user_account['score'] += self.score
            else:
                messagebox.showinfo("結果", "電腦抓對了！")
                self.player.lose_dice()

# =============================================================================
#     
# 
#     def challenge(self):
#         if not self.previous_call:
#             messagebox.showerror("錯誤", "你還沒報數抓什麼抓🙄！")
#             return
#     
#         count, value = self.previous_call
#         actual_count = sum(1 for p in self.all_players for d in p.dice if d == value or d == 1)
#     
#         # 攤牌顯示
#         result_text = f"場上骰子攤牌：\n玩家骰子：{self.player.dice}\n電腦骰子：{self.computer.dice}"
#         result_text += f"\n場上共有 {actual_count} 顆 {value}（含萬能數字 1）。"
#         messagebox.showinfo("攤牌結果", result_text)
#         
#         if actual_count >= count:
#             if self.current_turn == "player":
#                 messagebox.showinfo("結果", "玩家抓錯了！")
#                 self.player.lose_dice()
#             else:
#                 messagebox.showinfo("結果", "電腦抓錯了！")
#                 self.computer_losses += 1
#                 if self.computer_losses >= self.computer_loss_multiplier:
#                     self.computer.lose_dice()
#                     self.computer_losses = 0
#                     self.player.add_experience(200)  # 增加經驗值
#                #     self.score += 200
#                     self.user_account['score'] += 200  # 累計分數
#                     self.user_account['score'] += self.score
#         else:
#             if self.current_turn == "player":
#                 messagebox.showinfo("結果", "玩家抓對了！")
#                 self.computer_losses += 1
#                 if self.computer_losses >= self.computer_loss_multiplier:
#                     self.computer.lose_dice()
#                     self.computer_losses = 0
#                     self.player.add_experience(200)  # 增加經驗值
#                     self.user_account['score'] += 200  # 累計分數
#                     self.user_account['score'] += self.score
#             else:
#                 messagebox.showinfo("結果", "電腦抓對了！")
#                 self.player.lose_dice()
# =============================================================================


# =============================================================================
#         # 判定結果
#         if actual_count >= count:
#             if self.current_turn == "player":
#                 messagebox.showinfo("結果", "玩家抓錯了！")
#                 self.player.lose_dice()
#             else:
#                 messagebox.showinfo("結果", "電腦抓錯了！")
#                 self.computer_losses += 1
#                 if self.computer_losses >= self.computer_loss_multiplier:
#                     self.computer.lose_dice()
#                     self.computer_losses = 0
#                     self.player.add_experience(200)  # 增加經驗值
#                     self.score = self.score + 200
#                     #print("1")
#                     #self.user_account['score'] = self.user_account['score'] + score
#         else:
#             if self.current_turn == "player":
#                 messagebox.showinfo("結果", "玩家抓對了！")
#                 self.computer_losses += 1
#                 if self.computer_losses >= self.computer_loss_multiplier:
#                     self.computer.lose_dice()
#                     self.computer_losses = 0
#                     self.player.add_experience(200)  # 增加經驗值
#                     self.score = self.score + 200
#                     #print("2")
#                     #self.user_account['score'] = self.user_account['score'] + score
#             else:
#                 messagebox.showinfo("結果", "電腦抓對了！")
#                 self.player.lose_dice()
# =============================================================================
    
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
            # 玩家輸了，恢復原始分數
            self.game_over = True  # 設定遊戲結束
            messagebox.showinfo("遊戲結束", "你輸了！🪦🪦🪦")
            self.user_account['score'] = self.original_score  # 恢復分數至初始值
            self.root.quit()  # 結束遊戲主迴圈
        elif not self.computer.dice:
            # 玩家贏了，增加分數
            self.game_over = True  # 設定遊戲結束
            messagebox.showinfo("遊戲結束", "你贏了！🎉🎉🎉")
            self.user_account['score'] += self.player.experience
            self.user_account['score'] += 800  # 勝利獲得 800 分
            self.user_account['score'] += self.score  # 累計遊戲內計分
            self.root.quit()  # 結束遊戲主迴圈


# =============================================================================
#     def check_game_over(self):
#         if not self.player.dice:
#             messagebox.showinfo("遊戲結束", "你輸了！🪦🪦🪦")
#             self.score == 0
#             self.user_account['score'] == self.original_score  # 將分數還原為初始分數
#             self.root.quit()  # 結束遊戲主迴圈
#         elif not self.computer.dice:
#             messagebox.showinfo("遊戲結束", "你贏了！🎉🎉🎉")
#             self.user_account['score'] += 800  # 累計分數
#        #     self.score += 800
#             self.user_account['score'] += self.score  # 累計分數
#             self.root.quit()  # 結束遊戲主迴圈
# =============================================================================
            
# =============================================================================
#     def check_game_over(self):
#         if not self.player.dice:
#             messagebox.showinfo("遊戲結束", "你輸了！🪦🪦🪦")
#             self.restart_game()
#             self.get_exp()
#         elif not self.computer.dice:
#             messagebox.showinfo("遊戲結束", "你贏了！🎉🎉🎉")
#             self.player.add_experience(800)  # 增加經驗值
#             self.score += 800
#             self.user_account['score'] += 800  # 累計分數
#             self.restart_game()
# =============================================================================

    
# =============================================================================
#     def check_game_over(self):
#         if not self.player.dice:
#             messagebox.showinfo("遊戲結束", "你輸了！🪦🪦🪦")
#             self.restart_game()
#             self.get_exp()
#         elif not self.computer.dice:
#             messagebox.showinfo("遊戲結束", "你贏了！🎉🎉🎉")
#             self.restart_game()
#             self.player.add_experience(800)  # 增加經驗值
#             self.score = self.score + 800
#             #score = 800
#             #print("3")
#             self.user_account['score'] = self.user_account['score'] + self.score
#             #self.get_exp()
# =============================================================================

    def toggle_pause(self, event=None):
        self.game_paused = not self.game_paused
        if self.game_paused:
            # 建立暫停視窗
            self.pause_window = tk.Toplevel(self.root)
            self.pause_window.title("遊戲暫停")
            self.pause_window.geometry("300x150")
            self.pause_window.grab_set()  # 阻止與主視窗互動
    
            # 顯示暫停標籤
            label = tk.Label(self.pause_window, text="遊戲已暫停", font=("Arial", 14))
            label.pack(pady=20)
    
            # 添加繼續按鈕
            continue_button = tk.Button(
                self.pause_window, text="繼續遊戲", font=("Arial", 12),
                command=lambda: self.toggle_pause()  # 按下按鈕後繼續遊戲
            )
            continue_button.pack(pady=10)
    
        else:
            # 關閉暫停視窗並恢復互動
            if hasattr(self, "pause_window"):
                self.pause_window.destroy()
            self.root.focus_force()  # 將焦點返回主視窗

            
            
    def quit_game(self, event=None):
        if messagebox.askyesno("確認退出", "確定要退出遊戲嗎？"):
            # 確保分數在退出時已經累積完成
      #      self.user_account['score'] += self.score
            self.root.destroy()
            self.root.quit()



# =============================================================================
#     def restart_game(self):
#         """重啟遊戲，回到選擇難度畫面"""
#         if messagebox.askyesno("確認重啟", "確定要重啟遊戲嗎？"):
#             # 銷毀遊戲畫面
#             self.game_frame.destroy()
#     
#             # 顯示難度選擇畫面
#             self.difficulty_frame.pack(fill=tk.BOTH, expand=True)
# =============================================================================

# =============================================================================
#     def restart_game(self, event=None):
#         """重啟遊戲，回到選擇難度畫面"""
#         if messagebox.askyesno("確認重啟", "確定要重啟遊戲嗎？"):
#             # 銷毀遊戲畫面
#             self.game_frame.destroy()
#     
#             # 顯示難度選擇畫面
#             self.difficulty_frame.pack(fill=tk.BOTH, expand=True)
# =============================================================================

            
    def restart_game(self, event=None):
        """重啟遊戲，回到選擇難度畫面"""
        if messagebox.askyesno("確認重啟", "確定要重啟遊戲嗎？"):
            # 清除遊戲畫面的所有元件
            for widget in self.root.winfo_children():
                widget.destroy()
    
            # 重置遊戲狀態
            self.difficulty = None  # 清空難度選擇
            self.player = None
            self.computer = None
            self.previous_call = None
            self.current_turn = "player"
            self.computer_losses = 0
    
            # 回到難度選擇畫面
            self.create_ui()


    def get_exp(self):
        print(f"[DEBUG] 獲取玩家經驗值：{self.player.experience}")  # 調試輸出
        return self.player.experience

def run(user_account):
    root = tk.Tk()
    game = DiceGame(root,user_account)
    exp = game.get_exp()
    root.mainloop()


def run(user_account):
    root = tk.Tk()
    game = DiceGame(root, user_account)
    
    # 設定遊戲主迴圈
    root.mainloop()
    
    # 獲取遊戲的最終經驗值或分數
    #final_score = game.score  # 假設 DiceGame 的 score 屬性儲存總分
    #return final_score


