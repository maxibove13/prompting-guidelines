import pygame
import random

pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labyrinth Game")
FONT = pygame.font.Font(None, 24)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.color = (0, 255, 0)
        self.moves = 0
        self.collisions = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 72)  # Bigger font for 'Game Over'

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        moves_text = FONT.render(f"Moves: {self.moves}", 1, (0, 0, 255))
        screen.blit(moves_text, (10, 10))
        collisions_text = FONT.render(f"Collisions: {self.collisions}", 1, (255, 0, 0))
        screen.blit(collisions_text, (10, 40))

        if self.x == WIDTH - self.size and self.y == HEIGHT - self.size:
            finish_text = self.font.render("You made it!", True, (0, 255, 0))
            screen.blit(finish_text, (WIDTH // 2, HEIGHT // 2))


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.cell_size = 40

        for i in range(rows):
            row = []
            for j in range(cols):
                cell = Cell(i, j, self.cell_size)
                row.append(cell)
            self.grid.append(row)

        # Make a subset of cells walls
        for _ in range(rows * cols // 3):  # change this value to add more/less walls
            while True:
                i, j = random.randint(0, rows - 1), random.randint(0, cols - 1)
                cell = self.grid[i][j]
                if (
                    cell.color != (0, 0, 0)
                    and (i != 0 or j != 0)
                    and (i != rows - 1 or j != cols - 1)
                ):
                    cell.color = (0, 0, 0)  # black
                    break

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def check_collision(self, player):
        x, y = player.x // self.cell_size, player.y // self.cell_size
        if x >= self.cols or y >= self.rows or x < 0 or y < 0:
            return True
        cell = self.grid[y][x]
        if cell.color == (0, 0, 0):
            return True
        return False


class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.color = (255, 255, 255)  # default to white
        self.visited = False

    def draw(self):
        x = self.col * self.size
        y = self.row * self.size
        pygame.draw.rect(screen, self.color, (x, y, self.size, self.size))


def generate_maze(maze):
    # Prim's Algorithm
    start_cell = maze.grid[0][0]
    frontier = [(0, 1), (1, 0)]  # right, down
    while frontier:
        x, y = random.choice(frontier)
        frontier.remove((x, y))
        neighbors = [
            (nx, ny)
            for nx, ny in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
            if 0 <= nx < maze.rows and 0 <= ny < maze.cols and maze.grid[nx][ny].visited
        ]
        if neighbors:
            nx, ny = random.choice(neighbors)
            dx, dy = nx - x, ny - y
            maze.grid[x][y].visited = True
            if dx == -1:  # left
                maze.grid[x][y].walls[3] = maze.grid[nx][ny].walls[1] = False
            elif dx == 1:  # right
                maze.grid[x][y].walls[1] = maze.grid[nx][ny].walls[3] = False
            elif dy == -1:  # up
                maze.grid[x][y].walls[0] = maze.grid[nx][ny].walls[2] = False
            elif dy == 1:  # down
                maze.grid[x][y].walls[2] = maze.grid[nx][ny].walls[0] = False
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                if (
                    0 <= x + dx < maze.rows
                    and 0 <= y + dy < maze.cols
                    and not maze.grid[x + dx][y + dy].visited
                ):
                    frontier.append((x + dx, y + dy))


def main():
    maze = Maze(15, 20)
    generate_maze(maze)
    player = Player(0, 0)

    running = True


def main():
    maze = Maze(15, 20)
    generate_maze(maze)
    player = Player(0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_x, new_y = player.x, player.y
                direction = None
                if event.key == pygame.K_LEFT:
                    new_x -= player.size
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    new_x += player.size
                    direction = "right"
                elif event.key == pygame.K_UP:
                    new_y -= player.size
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    new_y += player.size
                    direction = "down"

                if maze.check_collision(Player(new_x, new_y)):
                    player.collisions += 1
                    collision_text = player.font.render("Collision!", True, (255, 0, 0))
                    screen.blit(collision_text, (WIDTH // 2, HEIGHT // 2))
                    pygame.display.update()
                    pygame.time.wait(2000)  # Wait 2 seconds before continuing

                    if player.collisions == 3:
                        screen.fill((0, 0, 0))  # Clear the screen
                        game_over_text = player.game_over_font.render(
                            "Game Over", True, (255, 0, 0)
                        )
                        screen.blit(
                            game_over_text, (WIDTH // 4, HEIGHT // 2)
                        )  # Adjusted position
                        pygame.display.update()
                        pygame.time.wait(3000)  # Wait 3 seconds before quitting
                        running = False
                else:
                    player.x = new_x
                    player.y = new_y
                    player.moves += 1

        if running:  # Don't clear the screen or draw if the game is over
            screen.fill((0, 0, 0))
            maze.draw()
            player.draw()
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
