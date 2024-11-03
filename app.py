import itertools
import time
import random

from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/telemetry_slow")
def telemetry_slow():
    def stream():
        data = [30, 60, 90, 60, 100, 50, 45, 20]
        for idx in itertools.count():
            data.append(random.randint(0, 100))
            data.pop(0)
            msg = f"data: <div class='sparkline'>{",".join(map(str,data))}</div>\n\n"
            yield msg
            time.sleep(1/6)

    return Response(stream(), mimetype="text/event-stream")

@app.route("/telemetry_fast")
def telemetry_fast():
    def stream():
        data = [30, 60, 90, 60, 100, 50, 45, 20]
        for idx in itertools.count():
            data.append(random.randint(0, 100))
            data.pop(0)
            msg = f"data: <div class='sparkline'>{",".join(map(str,data))}</div>\n\n"
            yield msg
            time.sleep(1/30)

    return Response(stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
