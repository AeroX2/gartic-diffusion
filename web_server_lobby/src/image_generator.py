from pathlib import Path
import time
from typing import Optional
from redis import Redis
from rq import Queue


from lobby import Lobby, User

q = Queue(connection=Redis(host="redis", port=6379))


def generate_next_images(lobby: Lobby) -> dict[User, str]:
    round = lobby.current_round()
    round_number = round.round_number

    responses = round.user_responses
    response_users = list(responses.keys())
    response_values = list(responses.values())

    start = time.time()
    job = q.enqueue("diffusion.generate_images", response_values)
    while job.result is None:
        time.sleep(0.1)
    print(f"It took {time.time() - start} seconds to generate")

    error: Optional[str]
    images_data: list[bytes]
    (error, images_data) = job.result
    if error is not None:
        print("Error has occured", error)

    items: dict[User, str] = {}
    for i, result in enumerate(images_data):
        user = response_users[i]

        image_dir_path = Path(
            f"../static/images/lobby_{lobby.uuid}/round_{round_number}"
        )
        image_dir_path.mkdir(parents=True, exist_ok=True)
        image_path = image_dir_path / f"player_{user.sid}.png"
        f = image_path.open("wb")
        f.write(result)
        f.close()

        items[user] = str(image_path)
    return items
