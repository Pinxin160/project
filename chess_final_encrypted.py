import tkinter as tk
from tkinter import messagebox
import random
import json
import datetime
import os
from cryptography.fernet import Fernet

class ChessGame:
    def __init__(self, root, piece_ranks, user_account, saved_last_game=None):
        self.root = root
        self.game_window = tk.Toplevel(self.root)  # 創建第二個視窗（遊戲視窗）
        self.game_window.title("Chinese Dark Chess Game")
        self.piece_ranks = piece_ranks
        self.user_account = user_account
        self.saved_last_game = saved_last_game
        self.key_filename = './chess_game_records/key.key'

        # Add buttons for "Pause", "Restart" and "Quit Game"
        self.bind_keys()
        
        # Create a canvas for the chessboard
        self.canvas = tk.Canvas(self.game_window, width=800, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click_event)  # 綁定事件
        
        # Initialize game state
        if not self.saved_last_game:
            self.initialize_game_state()
        else:
            self.load_game_state(self.saved_last_game)

        # Create a label to show the turn status at the bottom left corner
        self.game_window.after(100)
        self.turn_label = tk.Label(self.game_window, text=f"目前輪到: ", font=("Arial", 14))
        # self.turn_label.place(x=10, y=self.game_window.winfo_height() - 30)  # 位置放置在左下角
        self.turn_label.place(x=10, y=370)  # 直接指定標籤的絕對位置
        self.game_window.update_idletasks()
        self.game_window.geometry(f"{self.game_window.winfo_width()}x{self.game_window.winfo_height()}+{self.game_window.winfo_x()}+{self.game_window.winfo_y()}")

        # 當遊戲視窗被關閉時，關閉主視窗
        self.game_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.game_window.destroy()  # 關閉遊戲視窗
        self.root.destroy()  # 關閉主視窗

    def bind_keys(self):
        # Bind keys to actions
        self.game_window.bind('<k>', lambda event: self.pause_game())
        self.game_window.bind('<f>', lambda event: self.quit_game())
        self.game_window.bind('<r>', lambda event: self.restart_game())

    def pause_game(self):
        print("Pause game triggered")  # 調試輸出
        pause_window = tk.Toplevel(self.game_window)
        pause_window.title("暫停遊戲")
        pause_window.geometry("300x150")
        # pause_window.grab_set()  # 模態視窗，阻止對主視窗的操作

        label = tk.Label(pause_window, text="遊戲已暫停", font=("Arial", 14)) # 視窗標題
        label.pack(pady=20)
 
        continue_button = tk.Button(pause_window, text="繼續", font=("Arial", 12), command=lambda: self.resume_game(pause_window)) # 繼續按鈕
        continue_button.pack(pady=10)
       
    def resume_game(self, pause_window):
        pause_window.destroy()  # 關閉暫停視窗
        self.game_window.focus_force()  # 確保主視窗回到焦點
        print("Resuming game")  # 調試輸出
        self.bind_keys() # 確保按鍵綁定仍有效

    def quit_game(self):
        confirm = messagebox.askyesno("離開遊戲", "確定要離開遊戲嗎？")
        if confirm:
            self.save_game_state()
            self.root.destroy()

    def restart_game(self):
        confirm = messagebox.askyesno("重新開始", "確定要重新開始遊戲嗎？")
        if confirm:
            self.canvas.delete("all")  
            self.initialize_game_state()
            messagebox.showinfo("遊戲重新開始", "遊戲已重新開始！")

    def generate_key(self): # 生成一個密鑰（只需要一次，並妥善保存）
        return Fernet.generate_key()

    def save_key(self, key, filename): # 將密鑰保存到檔案
        with open(filename, "wb") as key_file:
            key_file.write(key)

    def load_key(self, filename): # 從檔案讀取密鑰
        with open(filename, "rb") as key_file:
            return key_file.read()

    def save_game_state(self):
        game_state = {
            "pieces": self.pieces,  # 棋子狀態
            "death_pieces_player": self.death_pieces_player,
            "death_pieces_computer": self.death_pieces_computer,
            "player_color": self.player_color,
            "computer_color": self.computer_color,
            "current_turn": self.current_turn,
            "game_over": self.game_over,
            "no_capture": self.no_capture,
            "cnt": self.cnt,
        }

        os.makedirs('./chess_game_records', exist_ok=True)
        today = str(datetime.datetime.now().month) + str(datetime.datetime.now().day)

        if not os.path.exists(self.key_filename):
            key = self.generate_key()  # 密鑰不存在的話生成新密鑰
            self.save_key(key, self.key_filename)  # 保存密鑰
        else:
            key = self.load_key(self.key_filename)  # 讀取已存在的密鑰

        # 使用密鑰來加密遊戲狀態
        fernet = Fernet(key)
        game_state_json = json.dumps(game_state, ensure_ascii=False, indent=4)
        encrypted_data = fernet.encrypt(game_state_json.encode())

        # 將加密的資料儲存為檔案
        with open(f'./chess_game_records/{self.user_account}.encrypted', "wb") as f:
        # with open(f'./chess_game_records/{today}_usertest.encrypted', "wb") as f:
            f.write(encrypted_data)

    def draw_chessboard(self):
        """Draws a 4x8 chessboard."""
        square_width = 100
        square_height = 100
        for row in range(4):
            for col in range(8):
                x1 = col * square_width
                y1 = row * square_height
                x2 = x1 + square_width
                y2 = y1 + square_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#EEE", outline="#000")

    def redraw_chessboard(self): 
        self.canvas.delete("all")  # 清除棋盤
        self.draw_chessboard()     # 重新繪製棋盤
        for piece_id, piece in self.pieces.items():
            x, y = self.pieces[piece_id]["position"][0], self.pieces[piece_id]["position"][1]
            if self.pieces[piece_id]["reveal"]:  # if revealed
                revealed_piece = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill="white", outline="black")
                label = self.canvas.create_text(x, y, text=self.pieces[piece_id]["name"], fill=self.pieces[piece_id]["color"], font=("Helvetica", 20, "bold"))
                self.pieces[piece_id]["canvas_id"] = revealed_piece
                self.pieces[piece_id]["text_id"] = label
            else: # if not revealed
                self.pieces[piece_id]["canvas_id"] = self.create_facedown_piece(x, y)

    def load_game_state(self, file_name):
        print("檔案名稱: ", file_name)
        if not os.path.exists(file_name):
            messagebox.showinfo("遊戲繼續", "未找到存檔，開始新遊戲。")
            self.initialize_game_state()
            return
            # raise FileNotFoundError
        if not os.path.exists(self.key_filename):
            messagebox.showinfo("遊戲繼續", "密鑰檔案不存在，無法解密。")
            self.initialize_game_state()
            return
            # raise FileNotFoundError
        try:
            key = self.load_key(self.key_filename)  # 讀取已存在的密鑰
            fernet = Fernet(key)

            with open(file_name, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8") # 解密資料
            game_state = json.loads(decrypted_data) # 將解密後的資料轉換為 JSON 物件

            # 恢復遊戲狀態
            self.pieces = game_state["pieces"]
            self.death_pieces_player = game_state["death_pieces_player"]
            self.death_pieces_computer = game_state["death_pieces_computer"]
            self.player_color = game_state["player_color"]
            self.computer_color = game_state["computer_color"]
            self.current_turn = game_state["current_turn"]
            self.game_over = game_state["game_over"]
            self.no_capture = game_state["no_capture"]
            self.cnt = game_state["cnt"]
            self.selected_piece_id = None
            self.redraw_chessboard() # 更新畫面
            messagebox.showinfo("遊戲繼續", "遊戲狀態已成功恢復！")

        except Exception as e:
            # 刪除被竄改的檔案
            try:
                os.remove(file_name)
                messagebox.showinfo("遊戲繼續", f"損壞的存檔已刪除：{file_name}")
            except Exception as delete_error:
                messagebox.showinfo("遊戲繼續", f"無法刪除損壞的存檔：{delete_error}")

            self.initialize_game_state()
            
    def initialize_game_state(self):
        """Initialize the chess pieces and place them on the board."""
        self.pieces = {}
        self.death_pieces_player = {}
        self.death_pieces_computer = {}
        self.player_color = None  # Player's color
        self.computer_color = None  # Computer's color
        self.current_turn = "player"  # Current turn: "player" or "computer"
        # self.game_paused = False  # Game pause state
        self.game_over = False
        self.no_capture = 0
        self.selected_piece_id = None
        self.cnt = 0

        # Create all pieces
        red_pieces = ["仕", "相", "傌", "俥", "炮", "兵", "兵"]
        red_pieces_king = ["帥", "兵"]
        black_pieces = ["士", "象", "馬", "車", "包", "卒", "卒"]
        black_pieces_king = ["將", "卒"]
        all_pieces = red_pieces * 2 + red_pieces_king + black_pieces * 2 + black_pieces_king
        random.shuffle(all_pieces)  # Shuffle the pieces randomly

        self.draw_chessboard()
        piece_id = 1
        # Place pieces on the board
        for i, piece in enumerate(all_pieces):
            row, col = divmod(i, 8)
            x = col * 100 + 50
            y = row * 100 + 50
            color = "red" if piece in (red_pieces + red_pieces_king) else "black"

            # Store piece information, including unique ID
            self.pieces[piece_id] = {
                "name": piece,
                "color": color,
                "position": (x, y),
                "reveal": False,
                "canvas_id": None,
                "text_id": None
            }

            # Create the piece on the canvas
            self.pieces[piece_id]['canvas_id'] = self.create_facedown_piece(x, y)
            piece_id += 1

    def create_facedown_piece(self, x, y):
        """Create a facedown chess piece at a specific location."""
        piece = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill="green", outline="black", tags="marker")
        return piece

    def check_game_over(self):
        """檢查遊戲是否結束並處理結果"""
        if self.no_capture >= 50:
            result = "和局"
            player_score = 0
            message = f"雙方進行翻棋或移動棋子連續達 50 次: {result}，玩家得分為 {player_score} 。"
        elif len(self.death_pieces_computer) == 16:
            result = "玩家獲勝"
            player_score = 500 + 100 * (16 - len(self.death_pieces_player))
            message = f"{result}！玩家得分為 {player_score} 。"
        elif len(self.death_pieces_player) == 16:
            result = "電腦獲勝"
            player_score = 0
            message = f"{result}！玩家得分為 {player_score} 。"
        else:
            return  # 若未達結束條件，直接返回

        self.game_over = True
        messagebox.showinfo("遊戲結束", message)
        if self.saved_last_game:
            os.remove(self.saved_last_game)

    def handle_click_event(self, event):
        if self.game_over:  # 如果遊戲已結束，阻止操作
            return
        x, y = event.x, event.y
        self.handle_click(x, y)

    def handle_click(self, x, y):
        """Handle clicks on pieces."""
        if self.current_turn != "player":
            return  # Ignore clicks if it's not the player's turn
        x, y = self.closest_square_center((x, y))

        # 如果已經選擇了棋子，並且玩家點擊目標位置
        if self.selected_piece_id:
            print(f"選擇了棋子: {self.pieces[self.selected_piece_id]['name']}，位置: {self.pieces[self.selected_piece_id]['position']}")
            if self.pieces[self.selected_piece_id]['position'] == (x, y):
                self.selected_piece_id = None
                messagebox.showerror("錯誤", "取消選擇這顆選別顆。")
            elif self.move_piece(self.selected_piece_id, (x, y)):
                print("這回合結束。") 
                self.switch_turn()
            else:
                return

        else: # 如果還沒選擇棋子，選擇棋子
            print("請選擇一顆棋子。")
            selected_piece_info = None  # 修正：在迴圈外初始化 selected_piece_info，避免未定義問題
            for piece_id, info in self.pieces.items():
                px, py = info["position"]
                if abs(px - x) < 50 and abs(py - y) < 50:  # 點擊的是這顆棋子
                    self.selected_piece_id = piece_id
                    selected_piece_info = info
                    break        
            if not selected_piece_info:
                print(f"點擊位置 ({x}, {y}) 沒有棋子。")
                return
            if selected_piece_info["reveal"] and selected_piece_info["color"] != self.player_color: # 如果該棋子已揭示但不是玩家的棋子，請玩家重選一顆
                print(f"選擇了棋子: {selected_piece_info['name']}，位置: {selected_piece_info['position']}")
                self.selected_piece_id = None
                self.prompt_invalid_piece()
                return
            if selected_piece_info and selected_piece_info["reveal"] and selected_piece_info["color"] == self.player_color: # 如果該棋子已揭示並且是玩家的棋子，則選擇該棋子
                return
            elif not selected_piece_info["reveal"]: # 如果該棋子未揭示，執行揭示操作
                self.reveal_piece(self.selected_piece_id)
                print(f"在 ({x}, {y}) 翻開了一顆棋子: {self.pieces[self.selected_piece_id]['name']}")
                if self.player_color is None: # 如果是第一次揭示棋子時，設定玩家與電腦的顏色
                    self.player_color = selected_piece_info["color"]
                    self.computer_color = "red" if self.player_color == "black" else "black"
                    print(f"玩家顏色: {self.player_color}，電腦顏色: {self.computer_color}")
                self.switch_turn() # 移動後取消選擇的棋子，切換到電腦回合
        
    def reveal_piece(self, piece_id):
        """Reveal the piece at the specified location."""
        if self.pieces[piece_id] and not self.pieces[piece_id]["reveal"]:  # Check if piece exists and is not revealed
            # Remove the facedown piece
            self.canvas.delete(self.pieces[piece_id]["canvas_id"])
            
            # Update piece information
            self.pieces[piece_id]["reveal"] = True
            
            # Create the revealed piece
            revealed_piece = self.canvas.create_oval(self.pieces[piece_id]["position"][0] - 40, self.pieces[piece_id]["position"][1] - 40,
                                                     self.pieces[piece_id]["position"][0] + 40, self.pieces[piece_id]["position"][1] + 40,
                                                     fill="white", outline="black")
            label = self.canvas.create_text(self.pieces[piece_id]["position"][0], self.pieces[piece_id]["position"][1],
                                            text=self.pieces[piece_id]["name"], fill=self.pieces[piece_id]["color"], font=("Helvetica", 20, "bold"))
            self.pieces[piece_id]["canvas_id"] = revealed_piece
            self.pieces[piece_id]["text_id"] = label

    def is_within_board(self, position):
        x, y = position
        # 棋盤範圍是 (0, 0) 到 (800, 400)
        if 0 <= x <= 800 and 0 <= y <= 400:
            return True
        return False
    
    def get_piece_at_position(self, position):
        """Return the piece ID at a specific position, or None if empty."""
        x, y = position
        for piece_id, piece in self.pieces.items():
            px, py = piece["position"]
            if abs(px - x) < 40 and abs(py - y) < 40:  # 判斷是否在該棋子的範圍內
                return piece_id
        return None
    
    def closest_square_center(self, position, square_width=100, square_height=100, max_rows=4, max_cols=8):
        x, y = position
        col = int(x // square_width)
        row = int(y // square_height)
        col = max(0, min(col, max_cols - 1)) # 確保行和列在棋盤範圍內
        row = max(0, min(row, max_rows - 1)) # 確保行和列在棋盤範圍內
        center_x = int((col + 0.5) * square_width)
        center_y = int((row + 0.5) * square_height)
        return center_x, center_y
    
    def prompt_invalid_piece(self):
        messagebox.showerror("錯誤", "這不是你的棋子! 請重新選一顆。")
    
    def prompt_moving_warning(self):
        messagebox.showerror("錯誤", "移動無效，距離或方向違規。")

    def move_piece(self, from_piece_id, to_piece_position):
        """Move a piece from one position to another."""
        print("目前位置: ", self.pieces[from_piece_id]["position"])
        print("目標位置: ", to_piece_position)
        fx, fy = self.pieces[from_piece_id]["position"]
        tx, ty = to_piece_position
        target_piece_id = self.get_piece_at_position((tx, ty))
        
        # 1. 檢查目標位置是否在棋盤範圍內 (好像其實不會發生)
        if not self.is_within_board((tx, ty)):
            print(f"點擊位置 {(tx, ty)} 不在棋盤範圍內。")
            return False
        
        # 2. 檢查是否為合理的移動 (電腦操作不應該觸發這部分)
        if self.pieces[from_piece_id]["name"] in ["炮", "包"]:
            if not target_piece_id and (abs(fx - tx) > 100 or abs(fy - ty) > 100 or (abs(fx - tx) == 100 and abs(fy - ty) == 100)): # 移動的話只能一格、方向僅限水平和垂直
                self.prompt_moving_warning()
                return False
            elif target_piece_id and not self.cannon_validate_move(self.pieces[from_piece_id], self.pieces[target_piece_id]): # 吃子的話中間要有一顆棋子
                print("炮/包不符合吃子規則")
                self.prompt_moving_warning()
                return False
        else:
            if abs(fx - tx) > 100 or abs(fy - ty) > 100 or (abs(fx - tx) == 100 and abs(fy - ty) == 100): # 只能一格、方向僅限水平和垂直
                self.prompt_moving_warning()
                return False
        
        # 3. 檢查目標位置是否已有棋子
        if target_piece_id:  # 如果目標位置有棋子
            target_piece = self.pieces[target_piece_id]
            if not target_piece["reveal"]: # 如果目標棋子未揭示，先揭示再處理
                self.reveal_piece(target_piece_id)
                self.root.update()
                self.root.after(1000)
            if self.capture_piece(from_piece_id, target_piece_id): # 吃子成功後判斷是否還能吃
                if self.pieces[from_piece_id]['name'] in ["炮", "包"]:
                    if self.cannon_continue_capture(from_piece_id): # 如果可以繼續吃子讓玩家決定是否繼續
                        continue_eat = self.prompt_continue_eating() if self.current_turn == "player" else True
                        if continue_eat:
                            print("炮可以繼續吃子。")
                            self.cnt += 1
                            return False  # 返回，等待玩家點擊下一步動作
                        else:
                            return True  # 玩家結束操作
                    else:
                        print("炮無法繼續吃子，結束本次操作。")
                        return True  # 玩家結束操作
                else:
                    if self.continue_capture(from_piece_id):
                        continue_eat = self.prompt_continue_eating() if self.current_turn == "player" else True
                        if continue_eat:
                            print("可以繼續吃子")
                            self.cnt += 1
                            return False  # 返回，等待玩家點擊下一步動作
                        else:
                            return True  # 玩家結束操作
                    else:
                        print("無法繼續吃子，結束本次操作。")
                        return True  # 玩家結束操作
            else:
                print("未能成功吃子")
                self.no_capture += 1
                self.check_game_over()
            return True
        elif self.cnt != 0:
            print("玩家不能再移動了。")
            return True
         
        # 4. 更新棋子位置
        self.pieces[from_piece_id]["position"] = tx, ty

        # 5. 更新畫布
        dx, dy = tx - fx, ty - fy
        self.canvas.move(self.pieces[from_piece_id]["canvas_id"], dx, dy)
        self.canvas.move(self.pieces[from_piece_id]["text_id"], dx, dy)
        self.selected_piece = None  # 移動後取消選擇的棋子

        print("移動成功到空格。")
        return True
    
    def perform_capture(self, from_piece_id, target_piece_id):
        """移除被吃掉的棋子並更新攻擊方棋子的位置。"""
        tx, ty = self.pieces[target_piece_id]["position"]
        fx, fy = self.pieces[from_piece_id]["position"]
        
        # 移除被吃掉的棋子 + 記錄被吃掉的棋子
        self.canvas.delete(self.pieces[target_piece_id]["canvas_id"])
        self.canvas.delete(self.pieces[target_piece_id]["text_id"])
        if self.pieces[target_piece_id]['color'] == self.player_color:
            self.death_pieces_player[target_piece_id] = self.pieces[target_piece_id]  
        else:
            self.death_pieces_computer[target_piece_id] = self.pieces[target_piece_id]
        del self.pieces[target_piece_id]  # 更新棋盤，移除被吃的棋子

        # 更新攻擊方棋子的位置和畫布(棋盤)
        self.pieces[from_piece_id]["position"] = (tx, ty)
        self.canvas.move(self.pieces[from_piece_id]["canvas_id"], tx - fx, ty - fy)
        self.canvas.move(self.pieces[from_piece_id]["text_id"], tx - fx, ty - fy)
        self.canvas.update_idletasks()
        self.check_game_over() #吃掉後判斷是否其中一方已經沒旗子了
        if self.current_turn == 'computer': self.root.after(1000)
    
    def capture_piece(self, from_piece_id, target_piece_id):
        """Capture an opponent's piece based on piece rank and exceptions."""
        if self.pieces[target_piece_id]:
            attacking_piece = self.pieces[from_piece_id]  # 攻擊方棋子
            print("攻擊方棋子: ", attacking_piece)
            defending_piece = self.pieces[target_piece_id]  # 被攻擊方棋子
            print("被攻擊方棋子: ", defending_piece)
            
            # 如果兩者屬於同一顏色，不能吃子
            if attacking_piece["color"] == defending_piece["color"]:
                return False

            # 處理特殊例外1: 炮/包滿足兩者中間有一子就能吃
            if attacking_piece["name"] in ["炮", "包"] and self.cannon_validate_move(attacking_piece, defending_piece):
                self.perform_capture(from_piece_id, target_piece_id)
                print("炮 (包) 成功吃子~")
                return True
            
            # 處理特殊例外2：帥(將)不能吃卒(兵)，但“卒” (兵)可以吃“帥” (將)。
            if attacking_piece["name"] in ["帥", "將"] and defending_piece["name"] in ["卒", "兵"]:
                print("帥 (將) 不能吃 卒 (兵)")
                return False
            if attacking_piece["name"] in ["卒", "兵"] and defending_piece["name"] in ["帥", "將"]:
                self.perform_capture(from_piece_id, target_piece_id)
                print("卒 (兵) 成功吃掉 帥 (將)~")
                return True
            
            # 根據等級判斷是否能吃
            attacking_rank = self.piece_ranks[attacking_piece["name"]]
            defending_rank = self.piece_ranks[defending_piece["name"]]
            if attacking_rank >= defending_rank:
                self.perform_capture(from_piece_id, target_piece_id)
                print("成功吃子~")
                return True  # 成功吃子
            else:
                print("等級不夠高無法吃子...")
                return False  # 無法吃子

        # print("不知道發生什麼情況的無法吃子。")
        return False  # 無法吃子(應該不會有這個情況)
    
    def cannon_validate_move(self, cannon_piece, target_piece):
        """ 驗證在同一橫排或縱列上，炮和目標位置中間必須恰好有一個棋子。 """
        cx, cy = cannon_piece["position"]
        tx, ty = target_piece["position"]
        position = [piece["position"] for piece in self.pieces.values()]
        print(position)
        if cx == tx: # 位於同一縱列
            min_y, max_y = sorted([cy, ty])
            count = 0
            for y in range(min_y + 100, max_y - 10, 100): # 計算兩個棋子之間有多少棋子
                if any(tuple(piece["position"]) == (cx, y) for piece in self.pieces.values()):
                    # print(f"{(cx, y)} 有棋子 {self.get_piece_at_position((cx, y))}")
                    count += 1
            print("同一縱列: ", count)
            return count == 1 # 恰有一顆時回傳 True
        elif cy == ty:  # 位於同一橫排
            min_x, max_x = sorted([cx, tx]) # 計算兩個棋子之間有多少棋子
            count = 0
            for x in range(min_x + 100, max_x - 10, 100):
                if any(tuple(piece["position"]) == (x, cy) for piece in self.pieces.values()):
                    # print(f"{(x, cy)} 有棋子 {self.get_piece_at_position((x, cy))}")
                    count += 1
            print("同一橫排: ", count)
            return count == 1
        return False
    
    def cannon_continue_capture(self, cannon_id):
        directions = [(-100, 0), (100, 0), (0, -100), (0, 100)]
        cannon_piece = self.pieces[cannon_id]
        for dx, dy in directions:
            tx, ty = cannon_piece['position'][0], cannon_piece['position'][1]
            while True:
                tx, ty = tx + dx, ty + dy
                if self.is_within_board((tx, ty)):
                    target_piece_id = self.get_piece_at_position((tx, ty))
                    if target_piece_id:
                        target_piece = self.pieces[target_piece_id]
                        if self.cannon_validate_move(cannon_piece, target_piece): # 存在有可以吃的子
                            print("炮有可以吃的子。")
                            if not target_piece['reveal'] or (target_piece['color'] != cannon_piece['color']):
                                return target_piece_id
                    else:
                        continue
                else: # 超出棋盤範圍了
                    break
        return False

    def continue_capture(self, from_piece_id):
        current_piece = self.pieces[from_piece_id]
        if not current_piece:
            return False  # 如果沒有棋子返回 False (但照理來說不應該有這個情況)
        surrounding_pieces = self.get_surrounding_pieces(from_piece_id)  # 獲取四周的棋子
        for piece_id in surrounding_pieces:
            surrounding_piece = self.pieces[piece_id]
            if not surrounding_piece['reveal']: # 只要有未揭示的棋子就可以繼續吃
                return True
            if surrounding_piece['color'] != current_piece['color']: # 如果是敵方旗子就要判斷是否能吃
                if current_piece['name'] in ["卒", "兵"] and surrounding_piece['name'] in ["帥", "將"]:
                    return True
                elif current_piece['name'] in ["帥", "將"]: # 我方如果是帥/降，只要敵方不是卒/兵就可以繼續吃
                    if surrounding_piece['name'] not in ["卒", "兵"]:
                        return True
                else:
                    if self.piece_ranks[current_piece['name']] >= self.piece_ranks[surrounding_piece['name']]: # 我方棋子比敵方棋子大或同等可以繼續吃
                        return True
        return False # 經過以上判斷都沒有能吃的就回傳 False

    def get_surrounding_pieces(self, piece_id):
        """ 獲取指定棋子位置周圍的敵方棋子或未揭示棋子。"""
        directions = [(-100, 0), (100, 0), (0, -100), (0, 100)]
        surrounding_pieces = []
        current_position = self.pieces[piece_id]['position']
        for dx, dy in directions:
            tx, ty = current_position[0]+dx, current_position[1]+dy
            if self.is_within_board((tx, ty)):
                surrounding_piece_id = self.get_piece_at_position((tx, ty))
                if surrounding_piece_id: # 如果這個位置有棋子的話
                    if not self.pieces[surrounding_piece_id]['reveal'] or self.pieces[surrounding_piece_id]['color'] != self.pieces[piece_id]['color']:
                        surrounding_pieces.append(surrounding_piece_id)
        return surrounding_pieces
    
    def prompt_continue_eating(self):
        """彈出對話框讓玩家選擇是否繼續吃子。"""
        response = messagebox.askyesno("連續吃子", "是否要繼續吃子？")
        return response  # 返回 True 表示玩家選擇“是”，False 表示選擇“否”
    
    def sort_pieces(self, pieces):
        """ 根據棋子等級對 pieces 進行排序。"""
        pieces_name = [self.pieces[piece_id]['name'] for piece_id in pieces]
        pieces_reveal = [self.pieces[piece_id]['reveal'] for piece_id in pieces]
        computer_piece_ranks = self.piece_ranks.copy()
        computer_piece_ranks["包"] = computer_piece_ranks["炮"] = 11
        sorted_pieces = sorted(zip(pieces, pieces_name, pieces_reveal), 
                               key=lambda x: (x[2], computer_piece_ranks[x[1]] if x[2] else -1), reverse=True) # # 已揭示的棋子先按名稱對應的等級排序，未揭示排最後
        revealed_pieces_sorted, _, _ = zip(*sorted_pieces) # 解壓排序結果，返回排序後的棋子 ID
        return list(revealed_pieces_sorted)
    
    def switch_turn(self):
        self.selected_piece_id = None
        self.cnt = 0
        if self.current_turn == "player":
            self.current_turn = "computer"
            print("============================================")
            print("現在回合: ", self.current_turn)
            self.turn_label.config(text=f"目前輪到: {self.current_turn}")
            self.root.after(1000, self.computer_turn)
        else:
            self.current_turn = "player"
            self.turn_label.config(text=f"目前輪到: {self.current_turn}")
            print("============================================")
            print("現在回合: ", self.current_turn)

    def computer_turn(self):
        """Handle the computer's turn."""
        if self.game_over:  # 如果遊戲已結束，阻止操作
            return
        if self.current_turn != "computer":
            return
        
        # 1. 找出所有已翻開的電腦方棋子
        revealed_pieces = [piece_id for piece_id, info in self.pieces.items() if info["reveal"] and info["color"] == self.computer_color]
        revealed_pieces_name = [info['name'] for piece_id, info in self.pieces.items() if info["reveal"] and info["color"] == self.computer_color]
        print("電腦目前已翻開的棋子有: ", revealed_pieces_name)
        # self.root.after(1000)
        
        # 2. 如果有已翻開的棋子: 先嘗試吃子
        if revealed_pieces:
            revealed_pieces_sorted = self.sort_pieces(revealed_pieces) # 從等級最大的開始嘗試吃子
            for piece_id in revealed_pieces_sorted:
                current_piece = self.pieces[piece_id]
                print(f"目前嘗試用 {current_piece['name']} 進行吃子")
                change_current_piece = 1
                while change_current_piece > 0:
                    if current_piece['name'] in ["炮", "包"]:
                        if self.cannon_continue_capture(piece_id):
                            target_piece_id = self.cannon_continue_capture(piece_id)
                            target_piece = self.pieces[target_piece_id]
                            print("target_piece: ", target_piece)
                            if self.move_piece(piece_id, target_piece['position']): # 無法再繼續吃子，輪到玩家
                                print("電腦無法再吃子，輪到玩家。")
                                self.switch_turn()
                                return
                        else:
                            print(f"一開始 炮(包) 就沒有可以吃的子。")
                            change_current_piece = -1 # 一開始炮就沒有棋子可以吃時，換下一個 revealed_pieces
                    else:
                        surrounding_pieces = self.get_surrounding_pieces(piece_id) # 確認四周有哪些棋子
                        if surrounding_pieces:
                            surrounding_pieces_sorted = self.sort_pieces(surrounding_pieces) # 將欲攻擊的棋子按照等級排序，而未揭示的放最後
                            for idx, target_piece_id in enumerate(surrounding_pieces_sorted):
                                surrounding_piece = self.pieces[target_piece_id]
                                print("目標候選: ", surrounding_piece)
                                if surrounding_piece['reveal']: # 先吃已揭示的敵方棋子
                                    print("目標候選為已揭示的敵方棋子")
                                    can_capture = False # 判斷特殊吃子規則
                                    if self.piece_ranks[current_piece['name']] >= self.piece_ranks[surrounding_piece['name']]:
                                        if current_piece['name'] in ["帥", "將"] and surrounding_piece['name'] in ["卒", "兵"]:
                                            print("電腦: 帥(將) 不能吃 卒(兵)。")
                                        else:
                                            print("電腦: 我方棋子吃掉敵方棋子")
                                            can_capture = True
                                    elif current_piece['name'] in ["卒", "兵"] and surrounding_piece['name'] in ["帥", "將"]:
                                        print("電腦: 卒(兵) 吃 帥(將)")
                                        can_capture = True
                                    if can_capture:
                                        if self.move_piece(piece_id, surrounding_piece['position']): # 無法再繼續吃子，輪到玩家
                                            print("電腦無法再吃子，輪到玩家。")
                                            self.switch_turn()
                                            return
                                        else:
                                            break # piece_id 的位置更新後跳出 for 迴圈繼續執行 while 迴圈 
                                    else:
                                        print(f"{current_piece['name']} 沒辦法吃掉 {surrounding_piece['name']}。")
                                else: # 再吃未揭示的棋子
                                    print("目標候選為未揭示的棋子")
                                    if self.move_piece(piece_id, surrounding_piece['position']):
                                        print("電腦無法再吃子，輪到玩家。")
                                        self.switch_turn()
                                        return
                                    else:
                                        break # piece_id 的位置更新後跳出 for 迴圈繼續執行 while 迴圈   

                                if idx == (len(surrounding_pieces_sorted) - 1):
                                    print(f"用 {current_piece['name']} 進行吃子失敗。")
                                    change_current_piece = -1 # 前面都沒有成功吃子時，強制換下一個 revealed_pieces
                        else:
                            print(f"{current_piece['name']} 附近沒有可以吃的棋子。")
                            change_current_piece = -1 # 該棋子附近完全沒有其他棋子時，換下一個 revealed_pieces    
            
        # 3. 無法吃子則隨機選擇一顆移動或翻旗
        facedown_pieces_id = [piece_id for piece_id, info in self.pieces.items() if not info["reveal"]]
        move_candidate = revealed_pieces + facedown_pieces_id
        random.shuffle(move_candidate)
        if not move_candidate:
            print(f"沒有可以翻也沒有可以移的棋，輪到玩家回合。")
            self.switch_turn()
            return
        directions = [(-100, 0), (100, 0), (0, -100), (0, 100)]
        for piece_id in move_candidate:
            if self.pieces[piece_id]['reveal']: # 
                random.shuffle(directions)
                current_position = self.pieces[piece_id]['position']
                for dx, dy in directions:
                    tx, ty = current_position[0] + dx, current_position[1] + dy
                    if self.is_within_board((tx, ty)):
                        surrounding_piece_id = self.get_piece_at_position((tx, ty))
                        if not surrounding_piece_id:
                            if self.move_piece(piece_id, (tx, ty)):
                                print(f"將 {self.pieces[piece_id]['name']} 移動到 ({tx}, {ty})")
                                self.switch_turn()
                                return
            else:
                to_reveal_id = random.choice(facedown_pieces_id)
                self.reveal_piece(to_reveal_id)
                print(f"在 {self.pieces[to_reveal_id]['position']} 翻開了一顆棋子: {self.pieces[to_reveal_id]['name']}")
                self.switch_turn()
                return

def main(user_account, saved_last_game):
    piece_ranks = {
        "將": 10, "帥": 10,
        "士": 9, "仕": 9,
        "象": 8, "相": 8,
        "車": 7, "俥": 7,
        "馬": 6, "傌": 6,
        "包": 5, "炮": 5,
        "卒": 4, "兵": 4,
    }

    def on_start_game():
        """當按下開始遊戲按鈕時執行的邏輯"""
        # saved_last_game = "./result/1219_usertest"
        if saved_last_game:
            response = messagebox.askyesno("遊戲紀錄", "檢測到上一次的遊戲紀錄，是否要繼續遊戲？")
            if response:
                game = ChessGame(root, piece_ranks, user_account, saved_last_game)
                # game.continue_game()
            else:
                game = ChessGame(root, piece_ranks, user_account, saved_last_game=None)
                # game.start_new_game()
        else:
            # 如果沒有遊戲紀錄，直接開始新遊戲
            messagebox.showinfo("提示", "未檢測到遊戲紀錄，將開始新遊戲。")
            game = ChessGame(root, piece_ranks, user_account, saved_last_game=None)
        # root.destroy()
        root.withdraw()
            
    # 建立主視窗
    root = tk.Tk()
    root.title("Chinese Dark Chess")
    root.geometry("600x400")

    # 添加按鈕
    start_button = tk.Button(root, text="開始遊戲", command=on_start_game, font=("Arial", 16))
    start_button.pack(expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    user_account = 123 # 當時登入的使用者~~~
    folder_path = "./chess_game_records"
    file_name = f"{str(user_account)}.encrypted"

    if file_name in os.listdir(folder_path): # 找目前這個使用者是否有上一次的象棋遊戲紀錄，沒有的話就 = None ~~~
        saved_last_game = folder_path + "/" + file_name
        print(f"檔案 {file_name} 存在於資料夾 {folder_path} 中。")
    else:
        saved_last_game = None
        print(f"檔案 {file_name} 不存在於資料夾 {folder_path} 中。")

    main(user_account, saved_last_game)
