import cv2                                  # Імпорт бібліотеки CV2

def main():
    img = cv2.imread('C:\\Users\\POTUZHNYY\\Desktop\\1.jpg', cv2.IMREAD_COLOR) # Функція читання зображення

    if img is None:                                         # Перевірка на існування зображення за шляхом вище
        print("Error: Could not read the image file.")
        return

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)              # Переведення зображення з BGR(звичайний кольоровий простір cv2) у RGB
    xyz = cv2.cvtColor(rgb, cv2.COLOR_RGB2XYZ)              # Переведення зображення з RGB у XYZ
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)              # Переведення зображення з RGB у HSV
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)             # Переведення зображення з RGB у GRAY
    yuv = cv2.cvtColor(rgb, cv2.COLOR_RGB2YUV)              # Переведення зображення з RGB у YUV

    cv2.imshow('Original', img)  # Виведення звичайного зображення на екран
    cv2.imshow('RGB', rgb)  # Виведення зображення у RGB-просторі на екран
    cv2.imshow('HSV', hsv)  # Виведення зображення у HSV-просторі на екран
    cv2.imshow('XYZ', xyz)  # Виведення зображення у XYZ-просторі на екран
    cv2.imshow('GRAY', gray)  # Виведення зображення у GRAY-просторі на екран
    cv2.imshow('YUV', yuv)  # Виведення зображення у YUV-просторі на екран

    cv2.waitKey(0)                                      # Функція очікування дій користувача(Задля того, щоб зображення не закрилося миттєво)
    cv2.destroyAllWindows()                            # Функція закривання усіх вікон


if __name__ == '__main__':                     # Викликання функції main
    main()
