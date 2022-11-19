import time
import random
import uvicorn
import socketio
from threading import Thread
from typing import Any, Optional

from lobby import Lobby, User
from image_generator import generate_next_images

sio = socketio.AsyncServer(
    logger=False,
    engineio_logger=False,
    async_mode="asgi",
    cors_allowed_origins=["http://localhost:8080"],
)
app = socketio.ASGIApp(sio)

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


async def add_user_to_lobby(sid: str, lobby: Lobby, user: User):
    if not lobby.has_user(user):
        lobby.add_user(user)
        sio.enter_room(sid, lobby.uuid)
        await sio.save_session(sid, {"lobby_uuid": lobby.uuid, "username": user.name})
        print(f"User {user.name} added to uuid: {lobby.uuid}")

    await sio.emit("lobby_update", {"lobby": lobby.serialize()}, room=lobby.uuid, skip_sid=sid)


def remove_empty_lobby(lobby: Lobby):
    for code, other_lobby in code_to_lobby.items():
        if lobby == other_lobby:
            del code_to_lobby[code]
            valid_codes.append(code)
            break


@sio.event
async def disconnect(sid: str):
    session = await sio.get_session(sid)

    lobby_uuid = session["lobby_uuid"]
    lobby = uuid_to_lobby[lobby_uuid]
    user = User(session["username"])

    if lobby.has_user(user):
        lobby.remove_user(user)

        print(f"User {user.name} disconnected from: {lobby.uuid}")
        await sio.emit("lobby_update", {"lobby": lobby.serialize()}, room=lobby.uuid, skip_sid=sid)

        del uuid_to_lobby[lobby_uuid]
        if lobby.empty():
            remove_empty_lobby(lobby)


@sio.event
async def lobby_create(sid: str, data: dict[str, Any]):
    if "username" not in data:
        return {"error": "Not enough data for lobby_create"}

    lobby = Lobby()
    uuid_to_lobby[lobby.uuid] = lobby
    code, error = generate_code(lobby)
    if error is not None:
        return {"error": error}
    print(f"Lobby created with uuid: {lobby.uuid}")
    print(f"Generated code {code} for {lobby.uuid}")

    username = data["username"]
    await add_user_to_lobby(sid, lobby, User(username))

    return {"lobby": lobby.serialize(), "code": code}


@sio.event
async def lobby_join(sid: str, data: dict[str, Any]):
    if "username" not in data or "code" not in data:
        return {"error": "Not enough data for lobby_join"}

    code = data["code"]
    username = data["username"]
    if code in code_to_lobby:
        lobby = code_to_lobby[code]
        await add_user_to_lobby(sid, lobby, User(username))
        return {"lobby": lobby.serialize()}
    else:
        return {"error": "Invalid lobby code"}


@sio.event
async def lobby_start_game(_: str, data: dict[str, Any]):
    if "uuid" not in data:
        print("Not enough data for lobby_start_game")
        return

    # Could also do it through get_session
    lobby_uuid = data["uuid"]
    lobby = uuid_to_lobby[lobby_uuid]

    round_timer = 20  # int(data.get("round_timer", 20))
    lobby.new_game(round_timer)

    print(f"Starting game in {lobby.uuid}")
    await sio.emit("game_start", {}, room=lobby.uuid)

    sio.start_background_task(game_loop, lobby)


@sio.event
async def game_response(sid: str, data: dict[str, Any]):
    if "description" not in data:
        print("Not enough data for game_response")
        return

    description = data["description"]

    session = await sio.get_session(sid)
    lobby_uuid = session["lobby_uuid"]
    lobby = uuid_to_lobby[lobby_uuid]
    user = User(session["username"])

    lobby.add_response(user, description)


async def game_loop(lobby: Lobby):
    for _ in range(1, lobby.amount_of_rounds):
        await sio.sleep(lobby.round_timer)

        # Wait for all responses
        await sio.emit("game_next_state", {"state": "loading"}, room=lobby.uuid)
        await wait_until(lobby.all_responses_received, 5)

        print("Responses received", lobby.current_responses())

        # Generate images
        items = generate_next_images(lobby)
        items = list(items.items())

        # Start a new round
        new_round = lobby.new_round()
        shuffled_items = [items[i] for i in new_round.shuffle_indices]

        # Pass out the new images
        for user, imageUrl in shuffled_items:
            await sio.emit(
                "game_next_state",
                {"state": "describe", "imageUrl": imageUrl},
                room=user.sid,
            )

    await sio.emit("game_finish", {}, room=lobby.uuid)
    # del uuid_to_lobby[lobby.uuid]
    # remove_empty_lobby(lobby)


async def wait_until(somepredicate, timeout, period=1, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs):
            return True
        await sio.sleep(period)
    return False


if __name__ == "__main__":
    print("Lobby is starting")
    # Test image generation is working

    # print("Warming up the diffusion server...")
    # lobby = Lobby()
    # lobby.new_game(0)

    # user = User("1234", "")
    # lobby.add_user(user)
    # lobby.add_response(user, "A cow on the moon, munching some grass")
    # print(generate_next_images(lobby))
    # print("Image generated!")

    # lobby.new_round()
    # lobby.add_response(user, "An alien cat lapping up some milk")
    # print(generate_next_images(lobby))
    # print("Another Image generated!")

    print("Lobby has stated")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info", proxy_headers=True)
