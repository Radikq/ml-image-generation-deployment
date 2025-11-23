'''
Запускать Stable Diffusion в CI — долго и без GPU может упасть.
Поэтому на этом этапе можно сделать очень простой тест, который не грузит модель, а просто проверяет,
что модуль импортируется и что функции существуют.
'''

def test_import_model_module():
    import app.model as model
    assert hasattr(model, "load_model")
    assert hasattr(model, "generate_image")
