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

        thresh1 = cv2.threshold(gray_frame, 80, 255, cv2.THRESH_BINARY)[1] 
        thresh2 = cv2.threshold(gray_frame, 120, 255, cv2.THRESH_BINARY)[1]
        thresh3 = cv2.threshold(gray_frame, 180, 255, cv2.THRESH_BINARY)[1]

        cv2.imshow('Binaries1', thresh1)  # Вивід кадру відео на монітор з порогом <= 80
        cv2.imshow('Binaries2', thresh2)  # Вивід кадру відео на монітор з порогом <= 120
        cv2.imshow('Binaries3', thresh3)  # Вивід кадру відео на монітор з порогом <= 180

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Чекаємо натискання кнопки q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
