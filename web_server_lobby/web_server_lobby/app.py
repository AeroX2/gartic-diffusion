import random

from flask import Flask, jsonify, request
from flask_socketio import join_room, leave_room, SocketIO, emit
from lobby import Lobby, User

app = Flask(__name__)
socketio = SocketIO(
    app,
    logger=False,
    cors_allowed_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
)

user_lobby = {}


def add_user_to_lobby(lobby, user):
    user_lobby[request.sid] = lobby
    join_room(lobby)
    lobby.add_user(user)
    print(f"User {user.name} added to uuid: {lobby.uuid}")
    emit("lobby_update", lobby.serialize(), to=lobby.uuid)


valid_codes = [str(i) for i in range(10000, 99999)]
random.shuffle(valid_codes)


def generate_code(lobby):
    if len(valid_codes) > 0:
        code = valid_codes.pop()
        code_to_lobby[code] = lobby
        return (code, None)
    else:
        return (None, "Ran out of valid codes")


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@socketio.on("disconnect")
def socket_disconnect():
    if request.sid in user_lobby:
        lobby = user_lobby[request.sid]

        print(f"Request {request.sid} disconnected from: {lobby.uuid}")
        emit("lobby_update", lobby.serialize(), to=lobby.uuid)
        del user_lobby[request.sid]


code_to_lobby = {}


@socketio.event
def lobby_create(data):
    if "username" not in data:
        emit("lobby_join_response", {"error": "Not enough data"})
        return

    lobby = Lobby()
    code, error = generate_code(lobby)
    if error is not None:
        emit("lobby_create_response", {"error": error})
        return
    print(f"Lobby created with uuid: {lobby.uuid}")
    print(f"Generated code {code} for {lobby.uuid}")

    username = data["username"]
    add_user_to_lobby(lobby, User(username))

    emit("lobby_create_response", {"lobby": lobby.serialize(), "code": code})


@socketio.event
def lobby_join(data):
    if "username" not in data or "code" not in data:
        emit("lobby_join_response", {"error": "Not enough data"})
        return

    code = data["code"]
    username = data["username"]
    print(code_to_lobby)
    if code in code_to_lobby:
        lobby = code_to_lobby[code]
        add_user_to_lobby(lobby, User(username))
        emit("lobby_join_response", {"lobby": lobby.serialize()})
    else:
        emit("lobby_join_response", {"error": "Invalid lobby code"})


if __name__ == "__main__":
    socketio.run(app, debug=True)
