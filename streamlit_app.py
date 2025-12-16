import io
import os
import requests
import streamlit as st
from PIL import Image

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Stable Diffusion Generator", layout="centered")
st.title("Stable Diffusion: генерация по тексту")
st.caption("Frontend: Streamlit • Backend: FastAPI • Генерация в Colab (GPU)")

prompt = st.text_area("Prompt", value="a photograph of an astronaut riding a horse", height=90)

col1, col2 = st.columns(2)
with col1:
    steps = st.slider("Steps", 1, 75, 30)
    guidance = st.slider("Guidance scale", 1.0, 20.0, 7.5)
with col2:
    seed = st.number_input("Seed (0 = случайно)", min_value=0, value=0, step=1)
    size = st.selectbox("Размер", ["512x512", "768x768"])
w, h = map(int, size.split("x"))

if st.button("Сгенерировать", type="primary"):
    if not prompt.strip():
        st.error("Введите prompt")
        st.stop()

    payload = {
        "prompt": prompt,
        "num_inference_steps": int(steps),
        "guidance_scale": float(guidance),
        "seed": None if int(seed) == 0 else int(seed),
        "width": int(w),
        "height": int(h),
    }

    with st.spinner("Генерирую..."):
        r = requests.post(f"{API_URL}/generate", json=payload, timeout=600)

    if r.status_code != 200:
        st.error(f"Ошибка API: {r.status_code}\n{r.text}")
        st.stop()

    img = Image.open(io.BytesIO(r.content))
    st.image(img, caption="Результат", use_container_width=True)

    out = io.BytesIO()
    img.save(out, format="PNG")
    st.download_button("Скачать PNG", data=out.getvalue(), file_name="result.png", mime="image/png")
