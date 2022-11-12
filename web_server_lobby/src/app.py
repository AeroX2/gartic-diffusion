import time
import random
import uvicorn
import socketio
from threading import Thread
from typing import Any, Optional

from lobby import Lobby, User
from image_generator import generate_next_images

sio = socketio.AsyncServer()
app = socketio.ASGIApp(sio)

import logging

logging.getLogger("sio").setLevel(logging.ERROR)
logging.getLogger("engineio").setLevel(logging.ERROR)

code_to_lobby: dict[str, Lobby] = {}
valid_codes = [str(i) for i in range(10000, 99999)]
random.shuffle(valid_codes)


def generate_code(lobby: Lobby) -> tuple[Optional[str], Optional[str]]:
    if len(valid_codes) > 0:
        code = valid_codes.pop()
        code_to_lobby[code] = lobby
        return (code, None)
    else:
        return (None, "Ran out of valid codes")


uuid_to_lobby: dict[str, Lobby] = {}
sid_to_lobby: dict[str, Lobby] = {}


def add_user_to_lobby(lobby: Lobby, user: User):
    if not lobby.has_user(user):
        sid_to_lobby[user.sid] = lobby
        sio.enter_room(lobby.uuid)
        lobby.add_user(user)
        print(f"User {user.name} added to uuid: {lobby.uuid}")
    sio.sio.emit("lobby_update", {"lobby": lobby.serialize()}, to=lobby.uuid)


def remove_empty_lobby(lobby: Lobby):
    for code, other_lobby in code_to_lobby.items():
        if lobby == other_lobby:
            del code_to_lobby[code]
            valid_codes.append(code)
            break


@sio.on("disconnect")
def socket_disconnect(sid: str):
    user = User(sid, "")
    lobby = sid_to_lobby[sid]
    if lobby.has_user(user):
        lobby.remove_user(user)

        print(f"Request {sid} disconnected from: {lobby.uuid}")
        sio.emit("lobby_update", {"lobby": lobby.serialize()}, to=lobby.uuid)

        del sid_to_lobby[sid]
        if lobby.empty():
            remove_empty_lobby(lobby)


@sio.event
def lobby_create(sid: str, data: dict[str, Any]):
    if "username" not in data:
        sio.emit("lobby_join_response", {"error": "Not enough data"})
        return

    lobby = Lobby()
    uuid_to_lobby[lobby.uuid] = lobby
    code, error = generate_code(lobby)
    if error is not None:
        sio.emit("lobby_create_response", {"error": error})
        return
    print(f"Lobby created with uuid: {lobby.uuid}")
    print(f"Generated code {code} for {lobby.uuid}")

    username = data["username"]
    add_user_to_lobby(lobby, User(sid, username))

    sio.emit("lobby_create_response", {"lobby": lobby.serialize(), "code": code})


@sio.event
def lobby_join(sid: str, data: dict[str, Any]):
    if "username" not in data or "code" not in data:
        sio.emit("lobby_join_response", {"error": "Not enough data"})
        return

    code = data["code"]
    username = data["username"]
    if code in code_to_lobby:
        lobby = code_to_lobby[code]
        add_user_to_lobby(lobby, User(sid, username))
        sio.emit("lobby_join_response", {"lobby": lobby.serialize()})
    else:
        sio.emit("lobby_join_response", {"error": "Invalid lobby code"})


@sio.event
def lobby_start_game(sid: str, data: dict[str, Any]):
    if "uuid" not in data:
        print("Not enough data for lobby_start_game")
        return
    lobby_uuid = data["uuid"]
    rounds = int(data.get("rounds", 20))
    round_timer = int(data.get("round_timer", 60))

    lobby = uuid_to_lobby[lobby_uuid]
    lobby.amount_of_rounds = rounds
    lobby.round_timer = round_timer

    print(f"Starting game in {lobby_uuid}")
    sio.emit("game_start", {}, to=lobby_uuid)

    thread = Thread(target=game_loop, args=(lobby,))
    thread.start()


@sio.event
def game_response(sid: str, data: dict[str, Any]):
    if "description" not in data:
        print("Not enough data for game_response")
        return

    description = data["description"]

    lobby = sid_to_lobby[sid]
    lobby.add_response(User(sid, ""), description)


def game_loop(lobby: Lobby):
    for round_number in range(1, lobby.amount_of_rounds):
        time.sleep(lobby.round_timer)

        # Wait for all responses
        sio.emit("game_next_state", {"state": "loading"}, to=lobby.uuid)
        wait_until(lobby.all_responses_received, 5)

        # Generate images
        items = generate_next_images(lobby)

        # Pass out the new images
        for user, imageUrl in items.items():
            sio.emit(
                "game_next_state",
                {"state": "loading", "imageUrl": imageUrl},
                to=user.sid,
            )

        # Start a new round
        lobby.new_round(round_number)

    sio.emit("game_finish", {}, to=lobby.uuid)
    # del uuid_to_lobby[lobby.uuid]
    # remove_empty_lobby(lobby)


def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False


if __name__ == "__main__":
    print("Lobby is starting")
    # Test image generation is working

    print("Warming up the diffusion server...")
    lobby = Lobby()
    user = User("1234", "")
    lobby.add_user(user)
    lobby.add_response(user, "A cow on the moon, munching some grass")
    print(generate_next_images(lobby))
    print("Image generated!")

    lobby.new_round(1)
    lobby.add_response(user, "An alien cat lapping up some milk")
    print(generate_next_images(lobby))
    print("Another Image generated!")

    print("Lobby has stated")
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
