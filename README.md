<!DOCTYPE html>
<html>
<head>
    <title>Simple Browser Game</title>
    <style>
        #gameButton {
            padding: 20px 40px;
            font-size: 24px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        #gameButton:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <h1>Simple Game Example</h1>
    <button id="gameButton">Click to Play!</button>

    <script>
        // Simple game logic
        const button = document.getElementById('gameButton');
        let score = 0;

        button.addEventListener('click', () => {
            score++;
            button.textContent = `Score: ${score} 🎮`;
            button.style.transform = `scale(${1 + score*0.05})`;
        });
    </script>
</body>
</html>
