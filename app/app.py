from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, decode_responses=True)

@app.route("/vote/<option>", methods=["POST"])
def vote(option):
    r.incr(f"votes:{option}")
    return jsonify({"message": f"Vote recorded for {option}"})

@app.route("/results", methods=["GET"])
def results():
    keys = r.keys("votes:*")
    data = {k.split(":")[1]: int(r.get(k)) for k in keys}
    return jsonify(data)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
