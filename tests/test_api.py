from fastapi.testclient import TestClient
from PIL import Image
import app.model as model
from app.api import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_generate_mock(monkeypatch):
    def fake_generate_image(*args, **kwargs):
        return Image.new("RGB", (64, 64))

    monkeypatch.setattr(model, "generate_image", fake_generate_image)

    r = client.post("/generate", json={"prompt": "test"})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/png")
    assert len(r.content) > 10
