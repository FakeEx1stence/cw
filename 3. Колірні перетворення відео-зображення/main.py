import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():  # Перевірка на існування потоку відеозображення
        print("Error: Could not open the camera.")
        return

    while True:

        ret, frame = cap.read()  # Читання кадру відео

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)             # Переведення зображення у GRAY-простір
        cv2.imshow('OriginalFrame', frame)  # Вивід кадру відео на монітор
        cv2.imshow('GrayColoredFrame', gray_frame)  # Вивід кадру відео на монітор з кольоровим простором GRAY

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Чекаємо натискання кнопки q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
