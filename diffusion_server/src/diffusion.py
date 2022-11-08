import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "../stable-diffusion-v1-5", revision="fp16", torch_dtype=torch.float16
).to("cuda")


def generate_images(
    prompts: list[str], lobby_uuid: str, round: int, players: list[str]
):
    if len(prompts) != len(players):
        return "Prompts and player lengths do not match"

    try:
        image_dir_path = Path(f"images/lobby_{lobby_uuid}/round_{round}")
        image_dir_path.mkdir(parents=True, exist_ok=True)

        images = pipe(prompts).images
        for i, image in enumerate(images):
            image_path = image_dir_path / f"player{players[i]}.png"
            image.save(image_path)
    except Exception as e:
        return str(e)

    return None
