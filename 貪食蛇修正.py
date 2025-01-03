import pygame
import random
import json

# 初始化 Pygame
pygame.init()

# 畫面設定
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FPS = 10

# 顏色設定
BG_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
ITEMS = ["watermelon", "apple", "strawberry", "game"]

# 初始化畫布
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("貪吃蛇遊戲")

# 全域變數與遊戲狀態
snake = [(100, 100)]
snake_direction = "RIGHT"
items = []
score = 0
game_running = False
game_paused = False

# 玩家資料
player_data = {
    "level": 1,
    "experience": 0,
    "history_score": 0
}

# 計分物件與分數
items = []
score = 0

# 檢查是否已有關卡物件存在
def has_game_item():
    return any(item["type"] == "game" for item in items)

# 食物生成函數，限制一次最多出現一個關卡物件
def generate_item():
    if has_game_item():
        # 若已存在關卡物件，從選項中移除 "game"
        possible_items = ["watermelon", "apple", "strawberry"]
    else:
        # 否則關卡物件可以成為選項之一
        possible_items = ITEMS

    item_type = random.choice(possible_items)
    item_position = (
        random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
    )
    return {"type": item_type, "position": item_position}

# 初始化6個計分項目，始終保持 6 個
items = []
while len(items) < 6:
    new_item = generate_item()
    items.append(new_item)

# 全局變數設置
MAX_FPS = 20  # 最大幀率，蛇移動的最大速度
MIN_FPS = 10   # 最小幀率，最低速度
FPS_INCREASE_RATE = 1  # 每增加30分，增加1幀率

# 更新蛇的位置
def update_snake():
    global score, running, FPS

    # 根據分數調整FPS，分數越高，FPS越大
    FPS = min(MAX_FPS, MIN_FPS + (score // 30) * FPS_INCREASE_RATE)

    head_x, head_y = snake[0]
    if snake_direction == "UP":
        new_head = (head_x, head_y - CELL_SIZE)
    elif snake_direction == "DOWN":
        new_head = (head_x, head_y + CELL_SIZE)
    elif snake_direction == "LEFT":
        new_head = (head_x - CELL_SIZE, head_y)
    elif snake_direction == "RIGHT":
        new_head = (head_x + CELL_SIZE, head_y)

    if (
        new_head[0] < 0
        or new_head[0] >= SCREEN_WIDTH
        or new_head[1] < 0
        or new_head[1] >= SCREEN_HEIGHT
    ):
        game_over()
        return

    if new_head in snake:
        game_over()
        return

    snake_rect = pygame.Rect(new_head[0], new_head[1], CELL_SIZE, CELL_SIZE)
    for item in items:
        item_type = item["type"]
        item_x, item_y = item["position"]

        if item_type == "watermelon":
            item_rect = pygame.Rect(item_x, item_y, CELL_SIZE * 2, CELL_SIZE * 2)
        elif item_type == "apple":
            item_rect = pygame.Rect(item_x, item_y, int(CELL_SIZE * 1.5), int(CELL_SIZE * 1.5))
        elif item_type == "strawberry":
            item_rect = pygame.Rect(item_x, item_y, CELL_SIZE, CELL_SIZE)
        elif item_type == "game":
            item_rect = pygame.Rect(item_x, item_y, CELL_SIZE, CELL_SIZE)

        if snake_rect.colliderect(item_rect):
            items.remove(item)
            if item_type == "watermelon":
                score += 5
            elif item_type == "apple":
                score += 10
            elif item_type == "strawberry":
                score += 15
            elif item_type == "game":
                guess_number_game()
            items.append(generate_item())
            break
    else:
        snake.pop()

    snake.insert(0, new_head)

# 繪製計分項目
def draw_item(item):
    item_type = item["type"]
    item_x, item_y = item["position"]
    

    if item_type == "watermelon":
        pygame.draw.circle(screen, (0, 255, 0), (item_x + CELL_SIZE, item_y + CELL_SIZE), CELL_SIZE)
        pygame.draw.circle(screen, (255, 0, 0), (item_x + CELL_SIZE, item_y + CELL_SIZE), CELL_SIZE // 2)
    elif item_type == "apple":
        pygame.draw.circle(screen, (255, 0, 0), (item_x + int(CELL_SIZE * 0.75), item_y + int(CELL_SIZE * 0.75)), int(CELL_SIZE * 0.75))
        pygame.draw.rect(screen, (0, 128, 0), (item_x + int(CELL_SIZE * 0.3), item_y, CELL_SIZE // 2, CELL_SIZE // 4))
    elif item_type == "strawberry":
        pygame.draw.polygon(screen, (255, 0, 128), [
            (item_x + CELL_SIZE // 2, item_y),
            (item_x, item_y + CELL_SIZE),
            (item_x + CELL_SIZE, item_y + CELL_SIZE)
        ])
        pygame.draw.circle(screen, (0, 255, 0), (item_x + CELL_SIZE // 2, item_y), CELL_SIZE // 8)
    elif item_type == "game":
        pygame.draw.rect(screen, (255, 255, 0), (item_x, item_y, CELL_SIZE, CELL_SIZE))
# 顯示遊戲開始畫面
def show_start_screen():
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont(None, 65)
    title_text = font.render("Welcome to Snake Game", True, (255, 255, 255))
    instructions_text = pygame.font.SysFont(None, 45).render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # 等待玩家開始遊戲
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
# 遊戲結束畫面
def game_over():
    global running
    draw_game_state()
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    running = False
# 初始化遊戲狀態
def reset_game():
    global snake, snake_direction, items, score, game_running, game_paused
    snake = [(100, 100)]
    snake_direction = "RIGHT"
    items = [generate_item() for _ in range(6)]
    score = 0
    game_paused = False

# 繪製遊戲狀態
def draw_game_state():
    screen.fill(BG_COLOR)
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    for item in items:
        draw_item(item)

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# 遊戲結束畫面（增加重新開始選項）
def game_over():
    global game_running
    draw_game_state()
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 重新開始遊戲
                    reset_game()
                    return  # 跳出 game_over，返回主遊戲迴圈
                elif event.key == pygame.K_q:  # 離開遊戲
                    pygame.quit()
                    exit()

# 猜數字遊戲
def guess_number_game():
    global score
    answer = random.randint(1, 99)  # 隨機生成答案
    lower_bound, upper_bound = 0, 100
    attempts = 0
    max_attempts = 5
    font = pygame.font.SysFont(None, 36)
    input_text = ""  # 用於玩家輸入數字
    feedback = ""
    feedback_time = 0  # 用來記錄顯示反饋的時間

    # 顯示開始訊息
    screen.fill(BG_COLOR)
    title1 = font.render("Ultimate Password:", True, (255, 255, 255))
    title2 = font.render("Guess a number between 1 and 100", True, (255, 255, 255))
    screen.blit(title1, (SCREEN_WIDTH // 2 - title1.get_width() // 2, 50))
    screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 100))
    pygame.display.flip()
    pygame.time.wait(2000)  # 等待 2 秒

    while True:
        # 清空畫面並顯示遊戲界面
        screen.fill(BG_COLOR)
        title1 = font.render("Ultimate Password:", True, (255, 255, 255))
        title2 = font.render("Guess a number between 1 and 100", True, (255, 255, 255))
        range_text = font.render(f"Number Range: {lower_bound} - {upper_bound}", True, (255, 255, 255))
        attempts_text = font.render(f"Remaining Chances: {max_attempts - attempts}", True, (255, 255, 255))
        input_prompt = font.render("Enter your number: ", True, (255, 255, 255))
        input_display = font.render(input_text, True, (255, 255, 255))
        feedback_text = font.render(feedback, True, (255, 255, 255))

        # 繪製到畫面
        screen.blit(title1, (SCREEN_WIDTH // 2 - title1.get_width() // 2, 50))
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 100))
        screen.blit(range_text, (SCREEN_WIDTH // 2 - range_text.get_width() // 2, 150))
        screen.blit(attempts_text, (SCREEN_WIDTH // 2 - attempts_text.get_width() // 2, 200))
        screen.blit(input_prompt, (SCREEN_WIDTH // 2 - 150, 250))
        screen.blit(input_display, (SCREEN_WIDTH // 2 + 150, 250))  # 顯示玩家輸入的數字在提示語後面
        screen.blit(feedback_text, (SCREEN_WIDTH // 2 - feedback_text.get_width() // 2, 300))
        pygame.display.flip()

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 按 Enter 提交數字
                    if input_text.isdigit():
                        guess = int(input_text)
                        if lower_bound < guess < upper_bound:
                            attempts += 1
                            if guess == answer:
                                score += 10
                                feedback = "BINGO! +10 points"
                                game_over_message(feedback)
                                return
                            elif guess < answer:
                                lower_bound = guess
                                feedback = "Too low!"
                                feedback_time = pygame.time.get_ticks()  # 記錄顯示時間
                            else:
                                upper_bound = guess
                                feedback = "Too high!"
                                feedback_time = pygame.time.get_ticks()  # 記錄顯示時間
                        else:
                            feedback = "Please enter a number within the valid range!"
                            feedback_time = pygame.time.get_ticks()  # 記錄顯示時間
                    else:
                        feedback = "Please enter a valid number!"
                        feedback_time = pygame.time.get_ticks()  # 記錄顯示時間
                    
                    # 每次提交後清空數字
                    input_text = ""  # 清空輸入框，為下一輪輸入做準備

                elif event.key == pygame.K_BACKSPACE:  # 刪除輸入的最後一個字
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():  # 輸入數字
                    input_text += event.unicode

        # 顯示過 3 秒後清除反饋訊息
        if feedback and pygame.time.get_ticks() - feedback_time > 2000:
            feedback = ""

        # 超過最大嘗試次數
        if attempts >= max_attempts:
            score -= 2
            feedback = "FAIL >< Minus 2 points"
            game_over_message(feedback)
            return

# 顯示遊戲結束訊息
def game_over_message(message):
    font = pygame.font.SysFont(None, 72)
    screen.fill(BG_COLOR)
    result_text = font.render(message, True, (255, 255, 255))
    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2500)  # 停留 3 秒後返回遊戲

# 主遊戲迴圈
def main():
    global game_running, game_paused, snake, snake_direction, items, score

    # 顯示開始畫面
    show_start_screen()

    # 初始化遊戲
    snake = [(100, 100)]
    snake_direction = "RIGHT"
    items = [generate_item() for _ in range(6)]
    score = 0
    game_running = True

    clock = pygame.time.Clock()

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"

        update_snake()
        draw_game_state()
        clock.tick(FPS)

main()
