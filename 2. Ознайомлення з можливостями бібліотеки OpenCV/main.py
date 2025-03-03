import cv2                                  # Імпорт бібліотеки CV2

def main():
    img = cv2.imread('C:\\Users\\POTUZHNYY\\Desktop\\1.jpg', cv2.IMREAD_COLOR) # Функція читання зображення

    if img is None:                                         # Перевірка на існування зображення за шляхом вище
        print("Error: Could not read the image file.")
        return

    cv2.imshow('Original', img)                   # Виведення зображення на екран
    cv2.waitKey(0)                                      # Функція очікування дій користувача(Задля того, щоб зображення не закрилося миттєво)
    cv2.destroyAllWindows()                            # Функція закривання усіх вікон


    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()            # Читання кадру відео
        cv2.imshow('Camera', frame)     # Вивід кадру відео на монітор

        if cv2.waitKey(1) & 0xFF == ord('q'):         # Чекаємо натискання кнопки q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':                     # Викликання функції main
    main()
