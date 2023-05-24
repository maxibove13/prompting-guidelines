import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Labyrinth Game")

# Set up the maze
maze_width = 20
maze_height = 15
maze = [
    [
        {"north": True, "south": True, "east": True, "west": True}
        for y in range(maze_height)
    ]
    for x in range(maze_width)
]
visited = [[False for y in range(maze_height)] for x in range(maze_width)]

# Recursive backtracking algorithm to generate the maze
stack = [(0, 0)]
visited[0][0] = True
while stack:
    x, y = stack[-1]
    neighbors = []
    if x > 0 and not visited[x - 1][y]:
        neighbors.append((x - 1, y))
    if x < maze_width - 1 and not visited[x + 1][y]:
        neighbors.append((x + 1, y))
    if y > 0 and not visited[x][y - 1]:
        neighbors.append((x, y - 1))
    if y < maze_height - 1 and not visited[x][y + 1]:
        neighbors.append((x, y + 1))
    if neighbors:
        nx, ny = random.choice(neighbors)
        if nx < x:
            maze[x][y]["west"] = False
            maze[nx][ny]["east"] = False
        elif nx > x:
            maze[x][y]["east"] = False
            maze[nx][ny]["west"] = False
        elif ny < y:
            maze[x][y]["north"] = False
            maze[nx][ny]["south"] = False
        elif ny > y:
            maze[x][y]["south"] = False
            maze[nx][ny]["north"] = False
        visited[nx][ny] = True
        stack.append((nx, ny))
    else:
        stack.pop()

# Set up the character
character_x = 0
character_y = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_LEFT
                and not maze[character_x][character_y]["west"]
            ):
                character_x -= 1
            elif (
                event.key == pygame.K_RIGHT
                and not maze[character_x][character_y]["east"]
            ):
                character_x += 1
            elif (
                event.key == pygame.K_UP and not maze[character_x][character_y]["north"]
            ):
                character_y -= 1
            elif (
                event.key == pygame.K_DOWN
                and not maze[character_x][character_y]["south"]
            ):
                character_y += 1

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the maze
    for x in range(maze_width):
        for y in range(maze_height):
            if maze[x][y]["north"]:
                pygame.draw.line(
                    screen, (255, 255, 255), (x * 32, y * 32), ((x + 1) * 32, y * 32)
                )
            if maze[x][y]["south"]:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    (x * 32, (y + 1) * 32),
                    ((x + 1) * 32, (y + 1) * 32),
                )
            if maze[x][y]["east"]:
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    ((x + 1) * 32, y * 32),
                    ((x + 1) * 32, (y + 1) * 32),
                )
            if maze[x][y]["west"]:
                pygame.draw.line(
                    screen, (255, 255, 255), (x * 32, y * 32), (x * 32, (y + 1) * 32)
                )

    # Draw the character
    pygame.draw.rect(screen, (255, 0, 0), (character_x * 32, character_y * 32, 32, 32))

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
