from app.model import generate_image

def main():
    prompt = input("Введите описание изображения: ")
    img = generate_image(prompt)
    img.save("result.png")
    print("Сохранено в result.png")

if __name__ == "__main__":
    main()
