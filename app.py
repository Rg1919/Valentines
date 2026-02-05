from flask import Flask, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)


# --- AUTOMATIC UNLOCK LOGIC ---
def check_unlocked():
    # Set this to your local timezone (e.g., 'Asia/Kolkata', 'America/New_York')
    user_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(user_tz)

    # Unlocks if it is February 14th or later
    if now.month == 2 and now.day >= 14:
        return True
    return False


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>For My Bubu</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-pink: #ff4d6d;
            --soft-pink: #ffccd5;
            --dark-red: #c9184a;
        }

        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            overflow: hidden; 
            background: transparent; 
            font-family: 'Poppins', sans-serif;
            display: flex; justify-content: center; align-items: center;
        }

        .unlocked-bg {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://i.postimg.cc/wTNCHXRc/photo-6246689208437688278-y.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            z-index: -1; 
            animation: fadeIn 2s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .hearts-bg {
            position: absolute; width: 100%; height: 100%;
            z-index: 1; pointer-events: none;
        }

        #lock-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 77, 109, 0.95);
            z-index: 100; display: flex; flex-direction: column;
            justify-content: center; align-items: center; color: white;
            text-align: center;
        }

        .card {
            background: rgba(255, 255, 255, 0.9); 
            backdrop-filter: blur(5px);
            padding: 40px; border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            text-align: center; z-index: 10; max-width: 85%;
            border: 2px solid var(--soft-pink);
            animation: float 3s ease-in-out infinite;
        }

        h1 { font-family: 'Dancing Script', cursive; color: var(--dark-red); font-size: 2.5rem; margin-bottom: 20px; }
        p { color: #333; line-height: 1.6; font-size: 1.2rem; font-weight: 600; }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
    </style>
</head>
<body>

    <div class="hearts-bg" id="hearts-container"></div>

    {% if not unlocked %}
    <div id="lock-overlay">
        <h1 style="color: white; font-size: 4rem;">🔒</h1>
        <h2>This love is currently under lock and key...</h2>
        <p style="color: white;">Patience, Bubu! This heart opens only on <b>February 14th</b>.</p>
    </div>
    {% else %}
    <div class="unlocked-bg"></div>

    <div class="card">
        <h1>Happy Valentines day to my beautiful Bubu!</h1>
        <p>I love you the mostest ! <br><span style="color: #c9184a; font-size: 1.5rem;">Marry me soon !</span></p>
    </div>

    <script>
        const duration = 10 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 11 };

        function randomInRange(min, max) { return Math.random() * (max - min) + min; }

        const interval = setInterval(function() {
            const timeLeft = animationEnd - Date.now();
            if (timeLeft <= 0) return clearInterval(interval);
            const particleCount = 50 * (timeLeft / duration);
            confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
            confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
        }, 250);
    </script>
    {% endif %}

    <script>
        function createHeart() {
            const container = document.getElementById('hearts-container');
            const heart = document.createElement('div');
            heart.innerHTML = '❤️';
            heart.style.position = 'absolute';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.top = '100vh';
            heart.style.fontSize = Math.random() * 20 + 15 + 'px';
            heart.style.opacity = Math.random();
            heart.style.transition = 'transform 6s linear, opacity 6s linear';
            heart.style.zIndex = '5';
            container.appendChild(heart);
            setTimeout(() => {
                heart.style.transform = 'translateY(-110vh) rotate(' + (Math.random() * 360) + 'deg)';
                heart.style.opacity = '0';
            }, 100);
            setTimeout(() => { heart.remove(); }, 6500);
        }
        setInterval(createHeart, 300);
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, unlocked=check_unlocked())


if __name__ == '__main__':
    app.run(debug=True)