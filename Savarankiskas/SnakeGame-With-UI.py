import pygame
import sys
import random
import re

# Konstantos
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 15

class SnakeGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)] #sąrašas
        self.snake_direction = (0, 1)
        self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.obstacles = [(3, 2), (5, 5), (10, 10), (15, 15)]
        self.game_over = False




        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.background_color = (20, 20, 20)
        self.menu_color = (30, 30, 30)
        self.button_color = (50, 50, 50)
        self.button_hover_color = (70, 70, 70)
        self.button_text_color = WHITE

        self.menu_open = False
        self.button_selected = 0  # 0 for Resume, 1 for Restart, 2 for Exit

        self.button_width = 200
        self.button_height = 50
        self.button_x = (WIDTH - self.button_width) // 2
        self.resume_button_y = (HEIGHT // 2) - 100
        self.restart_button_y = (HEIGHT // 2) - 25
        self.exit_button_y = (HEIGHT // 2) + 50

    def write_score(self):
        with open("Results.txt", "a") as file:
            file.write(f"Score: {self.score}\n")

    def find_highest_score(self):
        highest_score = 0
        score_pattern = re.compile(r"Score: (\d+)") # reguliari išraiška

        try:
            with open("Results.txt", "r") as file:
                for line in file:
                    match = score_pattern.search(line)
                    if match:
                        score = int(match.group(1))
                        if score > highest_score:
                            highest_score = score
        except FileNotFoundError:
            open("Results.txt", "a").close()

        return highest_score

    def show_start_menu(self):
        start_menu_open = True
        menu_option_selected = 0  # 0 for Begin, 1 for History, 2 for Exit

        while start_menu_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu_option_selected = (menu_option_selected - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        menu_option_selected = (menu_option_selected + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if menu_option_selected == 0:
                            start_menu_open = False  # Begin the game
                        elif menu_option_selected == 1:
                            self.show_history()
                        elif menu_option_selected == 2:
                            pygame.quit()
                            sys.exit()

            self.screen.fill(self.background_color)
            self.render_start_menu(menu_option_selected)
            pygame.display.flip()
            self.clock.tick(FPS)

    def render_start_menu(self, selected_option):
        menu_text_font = pygame.font.Font(None, 50)
        menu_options = ["Begin", "History", "Exit"]

        for i, option in enumerate(menu_options):
            text_color = WHITE if i == selected_option else (150, 150, 150)
            label = menu_text_font.render(option, True, text_color)
            label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60 + i * 60))
            self.screen.blit(label, label_rect)

    def show_history(self):
        history_open = True
        while history_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        history_open = False

            self.screen.fill(self.background_color)
            self.render_history()
            pygame.display.flip()
            self.clock.tick(FPS)

    def render_history(self):
        history_font = pygame.font.Font(None, 30)
        start_y = 50
        try:
            with open("Results.txt", "r") as file:
                for line in file:
                    label = history_font.render(line.strip(), True, WHITE)
                    self.screen.blit(label, (50, start_y))
                    start_y += 30
        except FileNotFoundError:
            label = history_font.render("No history available.", True, WHITE)
            self.screen.blit(label, (50, start_y))

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if not self.menu_open:
                        if event.key == pygame.K_UP and self.snake_direction != (0, 1):
                            self.snake_direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.snake_direction != (0, -1):
                            self.snake_direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.snake_direction != (1, 0):
                            self.snake_direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.snake_direction != (-1, 0):
                            self.snake_direction = (1, 0)
                        elif event.key == pygame.K_ESCAPE:
                            self.menu_open = True
                    else:
                        if event.key == pygame.K_UP:
                            self.button_selected = (self.button_selected - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            self.button_selected = (self.button_selected + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if self.button_selected == 0:
                                self.menu_open = False
                            elif self.button_selected == 1:
                                self.reset_game()
                            elif self.button_selected == 2:
                                self.game_over = True

            if not self.menu_open:
                self.move_snake()
                self.check_collisions()
                self.render_game()
            else:
                self.render_menu()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake_direction = (0, 1)
        self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.obstacles = [(3, 2), (5, 5), (10, 10), (15, 15)]
        self.menu_open = False

    def move_snake(self):  #metodas/funkcija
        new_head = (
            (self.snake[0][0] + self.snake_direction[0]) % GRID_WIDTH,
            (self.snake[0][1] + self.snake_direction[1]) % GRID_HEIGHT,
        )
        self.snake.insert(0, new_head)

        if self.snake[0] == self.food:
            self.score += 1
            self.food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
        else:
            self.snake.pop()

    def check_collisions(self):
        if self.snake[0] in self.obstacles or self.snake[0] in self.snake[1:]:
            self.write_score()  # Įrašome rezultatą į failą
            highest_score = self.find_highest_score()
            print(f"Aukščiausias rezultatas: {highest_score}")
            self.menu_open = True

    def render_game(self):
        self.screen.fill(self.background_color)
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, BLUE, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (WIDTH - 100, 10))

    def render_menu(self):
        pygame.draw.rect(self.screen, self.menu_color, (self.button_x, self.resume_button_y, self.button_width, self.button_height))
        pygame.draw.rect(self.screen, self.menu_color, (self.button_x, self.restart_button_y, self.button_width, self.button_height))
        pygame.draw.rect(self.screen, self.menu_color, (self.button_x, self.exit_button_y, self.button_width, self.button_height))

        resume_text = self.font.render("Resume", True, self.button_text_color)
        restart_text = self.font.render("Restart", True, self.button_text_color)
        exit_text = self.font.render("Exit", True, self.button_text_color)

        if self.button_selected == 0:
            pygame.draw.rect(self.screen, self.button_hover_color, (self.button_x, self.resume_button_y, self.button_width, self.button_height))
        elif self.button_selected == 1:
            pygame.draw.rect(self.screen, self.button_hover_color, (self.button_x, self.restart_button_y, self.button_width, self.button_height))
        elif self.button_selected == 2:
            pygame.draw.rect(self.screen, self.button_hover_color, (self.button_x, self.exit_button_y, self.button_width, self.button_height))

        self.screen.blit(resume_text, (self.button_x + 30, self.resume_button_y + 10))
        self.screen.blit(restart_text, (self.button_x + 30, self.restart_button_y + 10))
        self.screen.blit(exit_text, (self.button_x + 30, self.exit_button_y + 10))

def main():
    game = SnakeGame()  # objektas
    game.show_start_menu()
    game.run()

if __name__ == "__main__":
    main()
