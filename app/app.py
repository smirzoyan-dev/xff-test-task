from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        "Remote-Addr": request.remote_addr
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
