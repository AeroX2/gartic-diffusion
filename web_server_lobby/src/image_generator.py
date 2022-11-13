from pathlib import Path
import time
from typing import Optional
from redis import Redis
from rq import Retry, Queue


from lobby import Lobby, User

q = Queue(connection=Redis(host="redis", port=6379))


def generate_next_images(lobby: Lobby) -> dict[User, str]:
    round = lobby.current_round()
    round_number = round.round_number

    responses = round.user_responses
    response_users = list(responses.keys())
    response_values = list(responses.values())

    start = time.time()
    job = q.enqueue("diffusion.generate_images", response_values, retry=Retry(max=3))

    status = job.get_status()
    while not (status == "finished" or status == "failed"):
        time.sleep(0.1)
        status = job.get_status()

    if status == "failed":
        print("Diffusion server timed out")
        return {}

    print(f"It took {time.time() - start} seconds to generate")

    error: Optional[str]
    images_data: list[bytes]
    (error, images_data) = job.result
    if error is not None:
        print("Error has occured", error)
        return {}

    items: dict[User, str] = {}
    for i, result in enumerate(images_data):
        user = response_users[i]

        image_dir_path = Path(
            f"/workdir/images/lobby_{lobby.uuid}/round_{round_number}"
        )
        image_dir_path.mkdir(parents=True, exist_ok=True)
        image_path = image_dir_path / f"player_{user.sid}.png"
        f = image_path.open("wb")
        f.write(result)
        f.close()

        items[user] = str(image_path)
    return items
