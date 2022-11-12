import io
import torch
from pathlib import Path
from typing import Optional
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "../stable-diffusion-v1-5", revision="fp16", torch_dtype=torch.float16
).to("cuda")


def generate_images(prompts: list[str]) -> tuple[Optional[str], Optional[list[bytes]]]:
    try:
        images = pipe(prompts).images
        images_data: list[bytes] = []
        for image in images:
            byteIO = io.BytesIO()
            image.save(byteIO, format="PNG")
            images_data.append(byteIO.getvalue())
        return None, images_data
    except Exception as e:
        return str(e), None
