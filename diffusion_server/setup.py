from diffusers import StableDiffusionPipeline

#User: gwrsipdwqodelsfqfl@tmmwj.com
#Pass: 4QFAURzCghfkQnJ
hf_token = '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'
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", use_auth_token=hf_token
)