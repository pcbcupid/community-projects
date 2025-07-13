import websocket
import threading

ESP32_IP = "ws://<your_IP>:81"  

ws = None

def init_ws():
    global ws
    try:
        ws = websocket.WebSocket()
        ws.connect(ESP32_IP)
        print("WebSocket connected")
    except Exception as e:
        print("WebSocket connection error:", e)

def send_brightness(val):
    global ws
    try:
        brightness = str(int(max(0, min(255, val))))
        if ws:
            ws.send(brightness)
    except Exception as e:
        print("WebSocket send error:", e)

# Start connection at startup
threading.Thread(target=init_ws, daemon=True).start()
