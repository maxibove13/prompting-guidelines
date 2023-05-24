// Set up the screen
const screen_width = 640;
const screen_height = 480;
const screen = document.createElement("canvas");
screen.width = screen_width;
screen.height = screen_height;
document.body.appendChild(screen);
const ctx = screen.getContext("2d");
ctx.font = "20px Arial";
ctx.fillStyle = "white";
ctx.textAlign = "center";
ctx.fillText("Loading...", screen_width / 2, screen_height / 2);

// Set up the maze
const maze_width = 20;
const maze_height = 15;
const maze = Array.from({ length: maze_width }, () =>
  Array.from({ length: maze_height }, () => ({
    north: true,
    south: true,
    east: true,
    west: true
  }))
);
const visited = Array.from({ length: maze_width }, () =>
  Array.from({ length: maze_height }, () => false)
);

// Recursive backtracking algorithm to generate the maze
const stack = [[0, 0]];
visited[0][0] = true;
while (stack.length) {
  const [x, y] = stack[stack.length - 1];
  const neighbors = [];
  if (x > 0 && !visited[x - 1][y]) {
    neighbors.push([x - 1, y]);
  }
  if (x < maze_width - 1 && !visited[x + 1][y]) {
    neighbors.push([x + 1, y]);
  }
  if (y > 0 && !visited[x][y - 1]) {
    neighbors.push([x, y - 1]);
  }
  if (y < maze_height - 1 && !visited[x][y + 1]) {
    neighbors.push([x, y + 1]);
  }
  if (neighbors.length) {
    const [nx, ny] = neighbors[Math.floor(Math.random() * neighbors.length)];
    if (nx < x) {
      maze[x][y].west = false;
      maze[nx][ny].east = false;
    } else if (nx > x) {
      maze[x][y].east = false;
      maze[nx][ny].west = false;
    } else if (ny < y) {
      maze[x][y].north = false;
      maze[nx][ny].south = false;
    } else if (ny > y) {
      maze[x][y].south = false;
      maze[nx][ny].north = false;
    }
    visited[nx][ny] = true;
    stack.push([nx, ny]);
  } else {
    stack.pop();
  }
}

// Set up the character
let character_x = 0;
let character_y = 0;

// Game loop
let running = true;
function gameLoop() {
  // Handle events
  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" && !maze[character_x][character_y].west) {
      character_x -= 1;
    } else if (event.key === "ArrowRight" && !maze[character_x][character_y].east) {
      character_x += 1;
    } else if (event.key === "ArrowUp" && !maze[character_x][character_y].north) {
      character_y -= 1;
    } else if (event.key === "ArrowDown" && !maze[character_x][character_y].south) {
      character_y += 1;
    }
  });

  // Clear the screen
  ctx.clearRect(0, 0, screen_width, screen_height);

  // Draw the maze
  for (let x = 0; x < maze_width; x++) {
    for (let y = 0; y < maze_height; y++) {
      if (maze[x][y].north) {
        ctx.beginPath();
        ctx.moveTo(x * 32, y * 32);
        ctx.lineTo((x + 1) * 32, y * 32);
        ctx.stroke();
      }
      if (maze[x][y].south) {
        ctx.beginPath();
        ctx.moveTo(x * 32, (y + 1) * 32);
        ctx.lineTo((x + 1) * 32, (y + 1) * 32);
        ctx.stroke();
      }
      if (maze[x][y].east) {
        ctx.beginPath();
        ctx.moveTo((x + 1) * 32, y * 32);
        ctx.lineTo((x + 1) * 32, (y + 1) * 32);
        ctx.stroke();
      }
      if (maze[x][y].west) {
        ctx.beginPath();
        ctx.moveTo(x * 32, y * 32);
        ctx.lineTo(x * 32, (y + 1) * 32);
        ctx.stroke();
      }
    }
  }

  // Draw the character
  ctx.fillStyle = "red";
  ctx.fillRect(character_x * 32, character_y * 32, 32, 32);

  // Update the screen
  requestAnimationFrame(gameLoop);
}
gameLoop();
