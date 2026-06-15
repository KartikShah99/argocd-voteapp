from flask import Flask, jsonify, render_template_string
import redis
import os

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, decode_responses=True)

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vote App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f4f4f9; }
        h1 { color: #333; }
        button {
            font-size: 18px; padding: 12px 24px; margin: 10px;
            border: none; border-radius: 8px; cursor: pointer;
            color: white;
        }
        .cats { background-color: #ff7f50; }
        .dogs { background-color: #4682b4; }
        #results { margin-top: 30px; font-size: 20px; color: #333; }
    </style>
</head>
<body>
    <h1>🐱 vs 🐶 - Vote Now!</h1>
    <button class="cats" onclick="vote('cats')">Vote Cats 🐱</button>
    <button class="dogs" onclick="vote('dogs')">Vote Dogs 🐶</button>

    <div id="results">Loading results...</div>

    <script>
        async function vote(option) {
            await fetch('/vote/' + option, { method: 'POST' });
            loadResults();
        }

        async function loadResults() {
            const res = await fetch('/results');
            const data = await res.json();
            let html = '<h3>Results</h3>';
            html += 'Cats 🐱: ' + (data.cats || 0) + '<br>';
            html += 'Dogs 🐶: ' + (data.dogs || 0);
            document.getElementById('results').innerHTML = html;
        }

        loadResults();
        setInterval(loadResults, 3000);
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_PAGE)

@app.route("/vote/<option>", methods=["POST"])
def vote(option):
    r.incr(f"votes:{option}")
    return jsonify({"message": f"Vote recorded for {option}"})

@app.route("/results", methods=["GET"])
def results():
    keys = r.keys("votes:*")
    data = {k.split(":")[1]: int(r.get(k)) for k in keys}
    return jsonify(data)

@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": "v3-cicd"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
