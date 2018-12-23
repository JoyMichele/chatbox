from flask import Flask, request, render_template
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json

from geventwebsocket.websocket import WebSocket

app = Flask(__name__)  # type:Flask

user_socket_dict = {}


@app.route("/ws/<user>")
def ws(user):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[user] = user_socket
    print(len(user_socket_dict), user_socket_dict)
    while 1:
        msg = user_socket.receive()
        print(msg)
        msg_dict = json.loads(msg)
        to_ussocket = user_socket_dict.get(msg_dict.get("to_user"))
        to_ussocket.send(json.dumps({"from_user": user, "to_user": msg_dict.get("to_user"), "msg": msg_dict.get("msg")}))


@app.route("/")
def index():
    return render_template("ws.html")


if __name__ == "__main__":
    http_serv = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()