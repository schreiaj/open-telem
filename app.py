import itertools
import threading
import time
import random
import numpy as np

from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

dataDic = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/telemetry")
def telemetry():
    frequency = request.args.get('hz', default=30, type=int)
    print(frequency)
    def stream():
        for idx in itertools.count():
            msgs = []
            for key,values in dataDic.items():
                norm = prepare_data_for_sparkline(np.array(values))
                dataString = ",".join(map(str,norm))
                msgs.append(f"event: {key}\ndata: <p class='sparkline' sse-swap='{key}'>{"{"}{dataString}{"}"}<br/>{values[-1]}</p>" )
            yield "\n\n".join(msgs) + "\n\n"
            time.sleep(1/frequency)
    return Response(stream_with_context(stream()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)


def prepare_data_for_sparkline(data:np.array) -> np.array:
    # this data needs to be between 0 and 100 as integers
    # This is just a function of the font used for sparklines
    minVal = np.min(data)
    copy = np.copy(data)
    copy = copy - minVal
    maxVal = np.max(copy)
    copy = copy / max(maxVal, 1)
    return (copy * 100).astype(int)
    



def fetch_data():
    events = ["voltage", "current", "ev1", "ev2", "ev3", "ev4", "ev5", "ev6", "ev7", "ev8", "ev9", "ev10"]
    data = np.zeros([len(events),11]).astype(int).tolist()   
    for idx,event in enumerate(events):
        dataDic[event] = data[idx]
    # This is the infinit loop that updates the data, replace inside it with your own data fetching code
    for i in itertools.count():
        
        for key,values in dataDic.items():
            values.append(values[-1] + random.randint(0, 1) - 0.5)
            if len(values) > 10:
                values.pop(0)
            dataDic[key] = values

        # This is the frequency of the data update, make sure to sleep for a bit
        time.sleep(1/30)
    
 
threading.Thread(target=fetch_data, daemon=True).start()

