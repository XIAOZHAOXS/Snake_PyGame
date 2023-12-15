"""
Author:赵文瑄
Date:2023.12.14
Power By Pycharm
"""
import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色常量
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# 设置游戏窗口尺寸
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 设置蛇身单元尺寸
BLOCK_SIZE = 20

# 设置游戏帧率
GAME_FPS = 15

# 蛇类
class Snake:
    def __init__(self):
        self.body = [[WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]]
        self.x_change = 0
        self.y_change = 0

    def update(self):
        head = [self.body[0][0] + self.x_change, self.body[0][1] + self.y_change]
        self.body.insert(0, head)
        return self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, x_change, y_change):
        self.x_change, self.y_change = x_change, y_change

    def check_collision(self, x, y):
        for segment in self.body[1:]:
            if segment == [x, y]:
                return True
        return False

# 食物类
class Food:
    def __init__(self):
        self.position = self._get_random_position()

    def _get_random_position(self):
        return [round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE]

    def spawn(self):
        self.position = self._get_random_position()

# 游戏类
class Game:
    def __init__(self):
        self.game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.font_main = pygame.font.SysFont(None, 50)
        self.font_score = pygame.font.SysFont(None, 35)
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def show_start_screen(self):
        start_screen = True
        while start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    start_screen = False

            self.game_window.fill(COLOR_BLACK)
            self.display_message("Snake Game", COLOR_GREEN, -50)
            self.display_message("Press Any Key to Start", COLOR_WHITE, 50)
            pygame.display.update()
            self.clock.tick(GAME_FPS)

    def display_message(self, msg, color, y_displace=0):
        text_surface = self.font_main.render(msg, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + y_displace)
        self.game_window.blit(text_surface, text_rect)

    def run(self):
        self.show_start_screen()
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction(-BLOCK_SIZE, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(BLOCK_SIZE, 0)
                    elif event.key == pygame.K_UP:
                        self.snake.change_direction(0, -BLOCK_SIZE)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(0, BLOCK_SIZE)

            self.snake.update()

            if self.snake.body[0][0] >= WINDOW_WIDTH or self.snake.body[0][0] < 0 or \
               self.snake.body[0][1] >= WINDOW_HEIGHT or self.snake.body[0][1] < 0 or \
               self.snake.check_collision(self.snake.body[0][0], self.snake.body[0][1]):
                self.display_message("Game Over", COLOR_RED, -50)
                self.display_message(f"Score: {self.score}", COLOR_GREEN, 10)
                pygame.display.update()
                pygame.time.wait(2000)
                game_over = True

            self.game_window.fill(COLOR_BLACK)

            # 绘制食物
            pygame.draw.rect(self.game_window, COLOR_RED, [self.food.position[0], self.food.position[1], BLOCK_SIZE, BLOCK_SIZE])

            # 绘制蛇
            for block in self.snake.body:
                pygame.draw.rect(self.game_window, COLOR_GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

            # 蛇吃到食物
            if self.snake.body[0] == self.food.position:
                self.food.spawn()
                self.snake.grow()
                self.score += 1

            # 显示分数
            score_text = self.font_score.render(f"Score: {self.score}", True, COLOR_WHITE)
            self.game_window.blit(score_text, [0, 0])

            pygame.display.update()
            self.clock.tick(GAME_FPS)

        pygame.quit()

# 主函数
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()