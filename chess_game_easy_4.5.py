import tkinter as tk
from tkinter import messagebox
import random
import json

class ChessGame:
    def __init__(self, root, piece_ranks, saved_last_game=None):
        self.root = root
        self.root.title("Chinese Chess Game")
        self.piece_ranks = piece_ranks
        self.saved_last_game = saved_last_game
        
        # Create a canvas for the chessboard
        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()
        
        # Draw the chessboard
        self.draw_chessboard()
        self.canvas.bind("<Button-1>", self.handle_click_event)  # 綁定事件
        
        # Initialize pieces and game state
        if not self.saved_last_game:
            self.pieces = {}
            self.death_pieces_player = {}
            self.death_pieces_computer = {}
            self.player_color = None  # Player's color
            self.computer_color = None  # Computer's color
            self.current_turn = "player"  # Current turn: "player" or "computer"
            self.game_paused = False  # Game pause state
            self.game_over = False
            self.no_capture = 0
            self.selected_piece_id = None
            self.cnt = 0
            self.initialize_pieces()
        else:
            self.load_game_state(self, self.saved_last_game)

        # Add buttons for "Pause" and "End Game"
        self.add_control_buttons()

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

    def load_game_state(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                game_state = json.load(f)
                
            # 恢復遊戲狀態
            self.pieces = game_state["pieces"]
            self.death_pieces_player = game_state["death_pieces_player"]
            self.death_pieces_computer = game_state["death_pieces_computer"]
            self.player_color = game_state["player_color"]
            self.computer_color = game_state["computer_color"]
            self.current_turn = game_state["current_turn"]
            self.no_capture = game_state["no_capture"]
            self.cnt = game_state["cnt"]
            
            # 更新畫面
            self.redraw_chessboard()
            print("遊戲狀態已成功恢復！")
        except FileNotFoundError:
            print("未找到存檔，開始新遊戲。")
        except Exception as e:
            print(f"無法載入遊戲狀態: {e}")

    def redraw_chessboard(self): #有可能不需要???
        self.canvas.delete("all")  # 清除棋盤
        self.draw_chessboard()     # 重新繪製棋盤
        
        # 繪製棋子
        for piece_id, piece in self.pieces.items():
            x, y = self.pieces[piece_id]["position"][0], self.pieces[piece_id]["position"][1]
            if self.pieces[piece_id]["reveal"]:  # if revealed
                revealed_piece = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill="white", outline="black")
                label = self.canvas.create_text(x, y, text=self.pieces[piece_id]["name"], fill=self.pieces[piece_id]["color"], font=("Helvetica", 20, "bold"))
                self.pieces[piece_id]["canvas_id"] = revealed_piece
                self.pieces[piece_id]["text_id"] = label
            else: # if not revealed
                self.pieces[piece_id]["canvas_id"] = self.create_facedown_piece(x, y)

    def initialize_pieces(self):
        """Initialize the chess pieces and place them on the board."""
        # Define piece types for red and black
        red_pieces = ["仕", "相", "傌", "俥", "炮", "兵", "兵"]
        red_pieces_king = ["帥", "兵"]
        black_pieces = ["士", "象", "馬", "車", "包", "卒", "卒"]
        black_pieces_king = ["將", "卒"]

        # Create all pieces
        all_pieces = red_pieces * 2 + red_pieces_king + black_pieces * 2 + black_pieces_king
        random.shuffle(all_pieces)  # Shuffle the pieces randomly

        # Assign a unique ID to each piece
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
    
    def add_control_buttons(self):
        # Create a frame for control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Pause button
        pause_button = tk.Button(button_frame, text="暫停", command=self.pause_game)
        pause_button.pack(side=tk.LEFT, padx=5)

        # quit game button
        end_button = tk.Button(button_frame, text="終止遊戲", command=self.quit_game)
        end_button.pack(side=tk.LEFT, padx=5)

    def pause_game(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            messagebox.showinfo("結束暫停", "遊戲已暫停，按'結束暫停'以繼續遊戲。")
        else:
            messagebox.showinfo("遊戲繼續", "遊戲繼續進行！")

    def quit_game(self):
        confirm = messagebox.askyesno("終止遊戲", "確定要終止遊戲嗎？")
        if confirm:
            self.save_game_state("saved_game.json")
            self.root.destroy()

    def save_game_state(self, file_name):
        game_state = {
            "pieces": self.pieces,  # 棋子狀態
            "death_pieces_player": self.death_pieces_player,
            "death_pieces_computer": self.death_pieces_computer,
            "player_color": self.player_color,
            "computer_color": self.computer_color,
            "current_turn": self.current_turn,
            "no_capture": self.no_capture,
            "cnt": self.cnt,
        }
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(game_state, f, ensure_ascii=False, indent=4)

    def check_game_over(self):
        if self.no_capture >= 50:
            self.game_over = True
            messagebox.showinfo("遊戲結束", "雙方進行翻棋或移動棋子連續達 50 次: 和局，玩家得分為 0。")
            return
        elif len(self.death_pieces_computer) == 16:
            self.game_over = True
            player_score = 500 + 100*(16 - len(self.death_pieces_player))
            messagebox.showinfo("遊戲結束", f"玩家獲勝！得分為 {player_score} 。")
            return
        elif len(self.death_pieces_player) == 16:
            messagebox.showinfo("遊戲結束", "電腦獲勝，玩家得分為 0 。")
            return
        
    def handle_click_event(self, event):
        if self.game_over:  # 如果遊戲已結束，阻止操作
            return
        x, y = event.x, event.y
        self.handle_click(x, y)

    def handle_click(self, x, y):
        """Handle clicks on pieces."""
        if self.current_turn != "player":
            return  # Ignore clicks if it's not the player's turn
        print("玩家進行了點擊")
        x, y = self.closest_square_center((x, y))

        # 如果已經選擇了棋子，並且玩家點擊目標位置
        if self.selected_piece_id:
            if self.pieces[self.selected_piece_id]['position'] == (x, y):
                print("玩家強制結束這回合。")
                self.selected_piece_id = None
                self.cnt = 0
                self.current_turn = "computer"
                self.root.after(1000, self.computer_turn)  # 延遲 1 秒後執行電腦的回合
            elif self.move_piece(self.selected_piece_id, (x, y)):
                print("這回合結束。") 
                self.selected_piece_id = None
                self.cnt = 0
                self.current_turn = "computer"
                self.root.after(1000, self.computer_turn)  # 延遲 1 秒後執行電腦的回合
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
                self.selected_piece_id = None
                self.prompt_invalid_piece()
                return
            if selected_piece_info and selected_piece_info["reveal"] and selected_piece_info["color"] == self.player_color: # 如果該棋子已揭示並且是玩家的棋子，則選擇該棋子
                return
            elif not selected_piece_info["reveal"]: # 如果該棋子未揭示，執行揭示操作
                self.reveal_piece(self.selected_piece_id)
                print(f"Revealed piece: {self.pieces[self.selected_piece_id]['name']} at {self.pieces[self.selected_piece_id]['position']}")
                if self.player_color is None: # 如果是第一次揭示棋子時，設定玩家與電腦的顏色
                    self.player_color = selected_piece_info["color"]
                    self.computer_color = "red" if self.player_color == "black" else "black"
                    print(f"玩家顏色: {self.player_color}，電腦顏色: {self.computer_color}")
                # 移動後取消選擇的棋子，切換到電腦回合
                self.no_capture += 1
                self.check_game_over()
                self.selected_piece_id = None
                self.current_turn = "computer"
                self.root.after(1000, self.computer_turn)
        
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
        fx, fy = self.pieces[from_piece_id]["position"]
        tx, ty = to_piece_position
        target_piece_id = self.get_piece_at_position((tx, ty))
        
        # 1. 檢查目標位置是否在棋盤範圍內
        if not self.is_within_board((tx, ty)):
            print(f"點擊位置 {(tx, ty)} 不在棋盤範圍內。")
            return False
        
        # 2. 檢查是否為合理的移動 
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
                self.no_capture = 0
                if self.pieces[from_piece_id]['name'] in ["炮", "包"]:
                    if self.cannon_continue_capture(from_piece_id):
                        continue_eat = self.prompt_continue_eating()
                        if continue_eat:
                            self.cnt += 1
                            self.root.after(1000)
                            return False  # 返回，等待玩家點擊下一步動作
                        else:
                            return True  # 玩家結束操作
                    else:
                        print("玩家無法吃子，結束本次操作。")
                        return True  # 玩家結束操作
                else:
                    if self.continue_capture(from_piece_id): # 如果可以繼續吃子讓玩家決定是否繼續
                        continue_eat = self.prompt_continue_eating()
                        if continue_eat:
                            self.cnt += 1
                            self.root.after(1000)
                            return False  # 返回，等待玩家點擊下一步動作
                        else:
                            return True  # 玩家結束操作
                    else:
                        print("無法繼續吃子，結束本次操作。")
                        return True  # 玩家結束操作
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
        # self.remove_original_marker(fx, fy) # 移除原位置的綠色圓形
        dx, dy = tx - fx, ty - fy
        self.canvas.move(self.pieces[from_piece_id]["canvas_id"], dx, dy)
        self.canvas.move(self.pieces[from_piece_id]["text_id"], dx, dy)
        self.selected_piece = None  # 移動後取消選擇的棋子

        # 6. 根據誰移動來切換回合
        if self.current_turn == "player":
            self.current_turn = "computer"
            self.root.after(1000, self.computer_turn)  # 延遲 1 秒後執行電腦的回合
        else:
            self.current_turn = "player"

        print("移動成功到空格。")
        return True
    
    def perform_capture(self, from_piece_id, target_piece_id):
        """移除被吃掉的棋子並更新攻擊方棋子的位置。"""
        tx, ty = self.pieces[target_piece_id]["position"]
        fx, fy = self.pieces[from_piece_id]["position"]
        
        # 移除被吃掉的棋子
        self.canvas.delete(self.pieces[target_piece_id]["canvas_id"])
        self.canvas.delete(self.pieces[target_piece_id]["text_id"])
        if self.pieces[target_piece_id]['color'] == self.player_color:
            self.death_pieces_player[target_piece_id] = self.pieces[target_piece_id]  # 記錄被吃掉的棋子
        else: # (self.pieces[target_piece_id]['color'] == self.computer_color:) 
            self.death_pieces_computer[target_piece_id] = self.pieces[target_piece_id]
        self.check_game_over()
        del self.pieces[target_piece_id]  # 更新棋盤，移除被吃的棋子

        # 更新攻擊方棋子的位置和畫布(棋盤)
        # self.remove_original_marker(fx, fy)  # 移除原位置的綠色圓形
        self.pieces[from_piece_id]["position"] = (tx, ty)
        self.canvas.move(self.pieces[from_piece_id]["canvas_id"], tx - fx, ty - fy)
        self.canvas.move(self.pieces[from_piece_id]["text_id"], tx - fx, ty - fy)
    
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
                return True
            
            # 處理特殊例外2：帥(將)不能吃卒(兵)，但“卒” (兵)可以吃“帥” (將)。
            if attacking_piece["name"] in ["帥", "將"] and defending_piece["name"] in ["卒", "兵"]:
                print("帥 (將) 不能吃 卒 (兵)")
                return False
            if attacking_piece["name"] in ["卒", "兵"] and defending_piece["name"] in ["帥", "將"]:
                print("卒 (兵) 可以吃 帥 (將)")
                self.perform_capture(from_piece_id, target_piece_id)
                return True
            
            # 根據等級判斷是否能吃
            attacking_rank = self.piece_ranks[attacking_piece["name"]]
            defending_rank = self.piece_ranks[defending_piece["name"]]
            if attacking_rank >= defending_rank:
                self.perform_capture(from_piece_id, target_piece_id)
                return True  # 成功吃子
            else:
                return False  # 無法吃子

        print("不知道發生什麼情況的無法吃子。")
        return False  # 無法吃子(應該不會有這個情況)
    
    def cannon_validate_move(self, cannon_piece, target_piece):
        """ 驗證在同一橫排或縱列上，炮和目標位置中間必須恰好有一個棋子。 """
        cx, cy = cannon_piece["position"]
        tx, ty = target_piece["position"]
        if cx == tx: # 位於同一橫排
            min_y, max_y = sorted([cy, ty])
            count = 0
            for y in range(min_y + 1, max_y): # 計算兩個棋子之間有多少棋子
                if any(piece["position"] == (cx, y) for piece in self.pieces.values()):
                    count += 1
            return count == 1 # 恰有一顆時回傳 True
        elif cy == ty:  # 位於同一縱列
            min_x, max_x = sorted([cx, tx]) # 計算兩個棋子之間有多少棋子
            count = 0
            for x in range(min_x + 1, max_x):
                if any(piece["position"] == (x, cy) for piece in self.pieces.values()):
                    count += 1
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
                        if self.cannon_validate_move(cannon_piece, target_piece):
                            if not target_piece['reveal'] or (target_piece['color'] != cannon_piece['color']):
                                return True
                    else:
                        continue
                else:
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
        """ 獲取指定棋子位置周圍的棋子。"""
        directions = [(-100, 0), (100, 0), (0, -100), (0, 100)]
        surrounding_pieces = []

        current_position = self.pieces[piece_id]['position']
        for dx, dy in directions:
            tx, ty = current_position[0]+dx, current_position[1]+dy
            if self.is_within_board((tx, ty)):
                surrounding_piece_id = self.get_piece_at_position((tx, ty))
                if surrounding_piece_id: # 如果這個位置有棋子的話
                    surrounding_pieces.append(surrounding_piece_id)

        return surrounding_pieces
    
    def prompt_continue_eating(self):
        """彈出對話框讓玩家選擇是否繼續吃子。"""
        response = messagebox.askyesno("連續吃子", "是否要繼續吃子？")
        return response  # 返回 True 表示玩家選擇“是”，False 表示選擇“否”

    def computer_turn(self):
        """Handle the computer's turn."""
        if self.game_over:  # 如果遊戲已結束，阻止操作
            return
        if self.current_turn != "computer":
            return
        print("============================================")
        print("現在回合: ", self.current_turn)
                 
        # Step 3: 如果沒有可以移動的棋子，翻開一顆未翻開的棋子
        facedown_pieces_id = [piece_id for piece_id, info in self.pieces.items() if not info["reveal"]]
        if facedown_pieces_id:
            to_reveal_id = random.choice(facedown_pieces_id)
            self.reveal_piece(to_reveal_id)
            print(f"Revealed piece: {self.pieces[to_reveal_id]['name']} at {self.pieces[to_reveal_id]['position']}")
            
        self.current_turn = "player"  # 切換回合
        print("============================================")
        print("現在回合: ", self.current_turn)
        return
        return
        
# Main loop
if __name__ == "__main__":
    piece_ranks = {
    "將": 10, "帥": 10,
    "士": 9, "仕": 9,
    "象": 8, "相": 8,
    "車": 7, "俥": 7,
    "馬": 6, "傌": 6,
    "包": 5, "炮": 5,
    "卒": 4, "兵": 4}
    root = tk.Tk()
    game = ChessGame(root, piece_ranks)
    root.mainloop()