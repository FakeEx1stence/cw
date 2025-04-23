import cv2

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():  # Перевірка читання камери
        print("Error: Could not read the camera.")
        return

    while True:

        ret, frame = cap.read()  # Читання кадру відео

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)             # Переведення зображення у GRAY-простір
        cv2.imshow('OriginalFrame', frame)  # Вивід кадру відео на монітор
        laplacian = cv2.Laplacian(
            frame, # Оригінальне зображення
            ddepth=cv2.CV_64F, # глибина зображення(64FLOAT)
            ksize = 3, # розмір ядра
            scale = 1, # масштаб
            delta = 0, # контрастність
            borderType=cv2.BORDER_CONSTANT # тип обробки
        )

        laplacian_abs = cv2.convertScaleAbs(laplacian)

        cv2.imshow('Laplacian', laplacian_abs)  # Вивід кадру відео з виділенними границями на монітор

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Чекаємо натискання кнопки q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
