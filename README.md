# Image Generation Service

Учебный проект: развёртывание предобученной модели генерации изображений (Stable Diffusion)
в облаке с доступом через Web (Streamlit) и API (FastAPI).

## Стек
- Python
- diffusers (Stable Diffusion)
- Streamlit
- FastAPI
- pytest
- GitHub Actions (CI)

## Установка

```bash
pip install -r requirements.txt
```

## Демонстрация модели (локально)

```bash
python -m app.demo_cli
```

Ввести текстовый prompt, результат сохранится в result.png.

## Тесты

```bash
pytest
```

## Структура проекта

```text
your-project/
├── app/
│   ├── __init__.py
│   ├── model.py          # работа с ML-моделью
│   ├── demo_cli.py       # простой скрипт для локального прогона
│   ├── streamlit_app.py  # пока заглушка под будущий Streamlit
│   └── api.py            # пока заглушка под будущий FastAPI
├── tests/
│   └── test_model.py     # простые тесты
├── requirements.txt
├── README.md
```
