import random

from flask import Flask, request
from flask_socketio import join_room, SocketIO, emit
from lobby import Lobby, User

app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins=["https://127.0.0.1:5173", "https://localhost:5173"],
)

import logging

logging.getLogger("socketio").setLevel(logging.ERROR)
logging.getLogger("engineio").setLevel(logging.ERROR)


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


valid_codes = [str(i) for i in range(10000, 99999)]
random.shuffle(valid_codes)


def generate_code(lobby):
    if len(valid_codes) > 0:
        code = valid_codes.pop()
        code_to_lobby[code] = lobby
        return (code, None)
    else:
        return (None, "Ran out of valid codes")


code_to_lobby = {}
sid_to_lobby = {}


def add_user_to_lobby(lobby, user):
    if request.sid not in sid_to_lobby:
        sid_to_lobby[request.sid] = (lobby, user)
        join_room(lobby.uuid)
        lobby.add_user(user)
        print(f"User {user.name} added to uuid: {lobby.uuid}")
    emit("lobby_update", {"lobby": lobby.serialize()}, to=lobby.uuid)


@socketio.on("disconnect")
def socket_disconnect():
    if request.sid in sid_to_lobby:
        lobby, user = sid_to_lobby[request.sid]
        lobby.remove_user(user)

        print(f"Request {request.sid} disconnected from: {lobby.uuid}")
        emit("lobby_update", {"lobby": lobby.serialize()}, to=lobby.uuid)
        del sid_to_lobby[request.sid]


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
    if code in code_to_lobby:
        lobby = code_to_lobby[code]
        add_user_to_lobby(lobby, User(username))
        emit("lobby_join_response", {"lobby": lobby.serialize()})
    else:
        emit("lobby_join_response", {"error": "Invalid lobby code"})


@socketio.event
def lobby_start_game(data):
    if "uuid" not in data:
        print("Not enough data for lobby_start_game")
        return
    lobby_uuid = data["uuid"]
    print(f"Starting game in {lobby_uuid}")
    emit("game_start", {}, to=lobby_uuid)


if __name__ == "__main__":
    socketio.run(app, debug=True)
