import socketio
import pyperclip
from win10toast import ToastNotifier

sio = socketio.Client()
toaster = ToastNotifier()

@sio.event
def connect():
    print('成功連接到伺服器')

@sio.on('new_code')
def on_new_code(data):
    message = data['message']
    pyperclip.copy(message)
    toaster.show_toast(
        "Verify-Courier",
        message+" 以複製到剪貼簿",
        duration=10,
        icon_path=None,
        threaded=True
    )

@sio.event
def disconnect():
    print('與伺服器斷開連接')

sio.connect('http://172.20.10.3:5000')

sio.wait()
