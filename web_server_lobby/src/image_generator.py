import time
from redis import Redis
from rq import Queue


from lobby import Lobby, User

q = Queue(connection=Redis(host='redis', port=6379))

def generate_next_images(lobby: Lobby) -> list[tuple[User, str]]:
    round = lobby.current_round()
    round_number = round.round_number
    responses = round.user_responses
    users = list(map(lambda u: u.sid, lobby.users))
    job = q.enqueue("diffusion.generate_images", list(responses.values()), lobby.uuid, round_number, users)

    while job.result is None:
        time.sleep(0.1)

    return job.result
