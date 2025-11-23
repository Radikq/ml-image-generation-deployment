from diffusers import StableDiffusionPipeline
import torch

_pipe = None  # лениво загружаем модель один раз

def load_model():
    global _pipe
    if _pipe is None:
        _pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16
        )
        _pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return _pipe

def generate_image(prompt: str):
    """
    Генерирует PIL.Image по текстовому описанию.
    """
    pipe = load_model()
    result = pipe(prompt)
    return result.images[0]