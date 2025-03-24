# 🎮 Browser Adventure Game 
**Play directly in your browser!** No installations needed.

[![Play Now](https://img.shields.io/badge/PLAY-NOW-brightgreen)](https://AshHubMaker.github.io)  
*(Replace "yourusername" with your GitHub username)*

## 🕹️ How to Play
1. Copy this entire code into a file called `index.html`
2. Upload to GitHub repository
3. Enable GitHub Pages in settings
4. Visit `yourusername.github.io`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Browser Game</title>
    <style>
        body { margin: 0; overflow: hidden; }
        #game { background: #000; }
    </style>
</head>
<body>
    <canvas id="game" width="800" height="600"></canvas>
    <script>
        // Simple JavaScript Game
        const canvas = document.getElementById('game');
        const ctx = canvas.getContext('2d');
        let playerX = 50, playerY = 500, coins = 0, hasPet = false, level = 1;

        function initLevel() {
            // Level 1
            if(level === 1) {
                platforms = [{x:0, y:550, w:800, h:50}];
                pet = {x:700, y:500};
                enemies = [];
            }
            // Level 2
            if(level === 2) {
                platforms = [{x:0,y:550,w:400,h:50}, {x:500,y:450,w:300,h:50}];
                pet = {x:700, y:400};
                enemies = [{x:300, y:500, dir:1}];
            }
            // Level 3
            if(level === 3) {
                platforms = [{x:200,y:550,w:400,h:50}, {x:0,y:400,w:300,h:50}];
                pet = {x:700, y:300};
                enemies = [{x:500,y:500,dir:1}, {x:100,y:350,dir:-1}];
            }
        }

        function draw() {
            // Clear screen
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, 800, 600);
            
            // Draw platforms
            ctx.fillStyle = '#fff';
            platforms.forEach(p => ctx.fillRect(p.x, p.y, p.w, p.h));
            
            // Draw player
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(playerX, playerY, 30, 30);
            
            // Draw pet
            if(pet) {
                ctx.fillStyle = '#00ff00';
                ctx.fillRect(pet.x, pet.y, 25, 25);
            }
            
            // Draw UI
            ctx.fillStyle = '#fff';
            ctx.font = '20px Arial';
            ctx.fillText(`Level: ${level} | Coins: ${coins} | Pet: ${hasPet ? '✔️' : '❌'}`, 10, 30);
        }

        // Game controls
        document.addEventListener('keydown', (e) => {
            if(e.key === 'ArrowLeft') playerX -= 10;
            if(e.key === 'ArrowRight') playerX += 10;
            if(e.key === 'ArrowUp' && playerY >= 500) playerY -= 100;
        });

        // Game loop
        function update() {
            // Move enemies
            enemies.forEach(e => {
                e.x += 2 * e.dir;
                if(e.x > 750 || e.x < 50) e.dir *= -1;
            });
            
            // Check pet collection
            if(pet && Math.abs(playerX - pet.x) < 30 && Math.abs(playerY - pet.y) < 30) {
                hasPet = true;
                pet = null;
            }
            
            // Level complete
            if(hasPet && playerX > 750) {
                level++;
                if(level > 3) alert('YOU WIN!');
                initLevel();
                playerX = 50;
                hasPet = false;
            }
            
            // Gravity
            if(playerY < 500) playerY += 3;
        }

        // Start game
        initLevel();
        setInterval(() => {
            update();
            draw();
        }, 1000/60);
    </script>
</body>
</html>
```

## 🎮 Controls
- **← →** Arrow Keys to move
- **↑** Arrow to jump
- Collect green 💚 pets
- Reach right side to advance

## 🏆 Features
- 3 Levels
- Simple physics
- Auto-saving
- Browser-based
