import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():  # Перевірка на існування зображення за шляхом вище
        print("Error: Could not read the camera image.")
        return

    while True:

        ret, frame = cap.read()  # Читання кадру відео

        # Змінна зсуву за оссю Y (значення > 0 - зсув вниз, значення < 0 - зсув уверх)
        shift_y = 400

        # Створюємо матрицю зсуву: [1, 0, dx(0, тому що зсув вертикальний)], [0, 1, dy]
        M = np.float32([[1, 0, 0], [0, 1, shift_y]])

        # Застосовуємо зсув за допомогою Афінного перетворення(орігінальне зображення, матриця зсуву, та розміри зображення(ширина, висота)
        shifted_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
        cv2.imshow('OriginalFrame', frame)  # Вивід кадру відео на монітор
        cv2.imshow('ShiftedFrame', shifted_frame)  # Вивід кадру відео на монітор

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Чекаємо натискання кнопки q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
