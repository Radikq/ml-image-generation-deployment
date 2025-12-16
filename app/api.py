# app/api.py
from __future__ import annotations

import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

import app.model as model

app = FastAPI(title="Stable Diffusion API", version="1.0.0")


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)
    num_inference_steps: int = Field(default=30, ge=1, le=75)
    guidance_scale: float = Field(default=7.5, ge=1.0, le=20.0)
    seed: int | None = Field(default=None, ge=0, le=2**32 - 1)
    width: int = Field(default=512, ge=256, le=1024, multiple_of=8)
    height: int = Field(default=512, ge=256, le=1024, multiple_of=8)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(req: GenerateRequest):
    img = model.generate_image(
        prompt=req.prompt,
        num_inference_steps=req.num_inference_steps,
        guidance_scale=req.guidance_scale,
        seed=req.seed,
        width=req.width,
        height=req.height,
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
