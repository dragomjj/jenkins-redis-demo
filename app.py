from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route("/")
def index():
    count = r.incr("page_views")
    return jsonify({
        "message": "Hello from Jenkins CI/CD + Redis",
        "page_views": count
    })

@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "ok", "redis": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "redis": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
