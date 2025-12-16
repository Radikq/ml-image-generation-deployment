# app/model.py
from __future__ import annotations

import threading
from typing import Optional

from PIL import Image
import torch

_pipe = None
_lock = threading.Lock()


def load_model(model_id: str = "CompVis/stable-diffusion-v1-4"):
    """
    Лениво загружает Stable Diffusion один раз.
    """
    global _pipe
    if _pipe is not None:
        return _pipe

    with _lock:
        if _pipe is not None:
            return _pipe

        from diffusers import StableDiffusionPipeline  # важно: ленивый импорт

        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32

        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
        )
        pipe = pipe.to(device)
        print("DEVICE:", device, "DTYPE:", pipe.unet.dtype)
        pipe.enable_attention_slicing()
        _pipe = pipe
        return _pipe


def generate_image(
    prompt: str,
    num_inference_steps: int = 30,
    guidance_scale: float = 7.5,
    seed: Optional[int] = None,
    width: int = 512,
    height: int = 512,
) -> Image.Image:
    """
    Возвращает PIL.Image по тексту.
    """
    pipe = load_model()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(int(seed))

    with torch.inference_mode():
        out = pipe(
            prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            width=width,
            height=height,
        )
    return out.images[0]
