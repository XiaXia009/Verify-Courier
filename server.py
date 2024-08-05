from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
VC_token = "test"

def extract_consecutive_numbers(message):
    return re.findall(r'\d{4,}', message)

@app.route('/', methods=['POST'])
def receive_code():
    token = request.headers.get('token')
    if token != VC_token:
        return jsonify({"status": "錯誤的token"}), 401

    data = request.json
    message = data.get('msg')
    print("原始訊息:", message)
    
    numbers = extract_consecutive_numbers(message)
    if numbers:
        for number in numbers:
            print("處理後的數字:", number)
            socketio.emit('new_code', {'message': number})
    else:
        return jsonify("該訊息應該不是驗證信"), 200
    
    return jsonify("成功轉發到電腦"), 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
