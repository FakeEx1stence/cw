import cv2
import numpy as np
import tkinter
from tkinter import messagebox


class PairedNumber(Exception):
    """Виключення для парних чисел"""
    pass
class InvalidThresholdError(Exception):
    """Виключення для обмеження числа яскравості пікселя"""
    pass

class Window1(tkinter.Frame):
    def __init__(self, parent):
        # settings

        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tkinter.BOTH, expand=1)
        self.config(bg="#000033")
        self.create_widgets()

        self.file_path = tkinter.StringVar(value="None")

        #objects
    def create_widgets(self):
        #initialization

        """ORIGINAL"""

        self.lb_og = tkinter.Label(self, text="Орігінальне зображення", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.checkbox_ogisEnabled = tkinter.BooleanVar(value=True)
        self.checkbox_OG = tkinter.Checkbutton(self, state = "disabled", variable = self.checkbox_ogisEnabled)

        """GRAY"""
        self.lb_gray = tkinter.Label(self, text="Фільтр GRAY", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.checkbox_grayisOn = tkinter.BooleanVar(value=False)
        self.checkbox_GRAY = tkinter.Checkbutton(self, variable=self.checkbox_grayisOn, onvalue=True, offvalue=False)
        """VERTICAL"""
        self.lb_oy = tkinter.Label(self,text="Вертикальне зміщення", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.lb_height_oy = tkinter.Label(self,text="Зміщення за оссю OY(> 0 - вниз, < 0 - уверх)", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.checkbox_oyisOn = tkinter.BooleanVar(value=False)
        self.checkbox_oy = tkinter.Checkbutton(self, variable=self.checkbox_oyisOn, onvalue=True, offvalue=False,
                                                 command=self.oy_acts)

        """BINARIZATION"""

        self.lb_bin = tkinter.Label(self, text="Бінарізація", bg="#000033", fg="#ADD8E6",
                                   font=("Helvetica", 12))
        self.checkbox_binisOn = tkinter.BooleanVar(value=False)
        self.checkbox_bin = tkinter.Checkbutton(self, variable=self.checkbox_binisOn, onvalue=True, offvalue=False,
                                               command=self.bin_acts)
        self.lb_thresh = tkinter.Label(self,text="Мінімальний поріг та максимальне число (0<x<256)",bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))

        """LAPLASIAN"""


        self.lb_lap = tkinter.Label(self, text="Виділення меж", bg="#000033", fg="#ADD8E6",
                                   font=("Helvetica", 12))
        self.checkbox_lapisOn = tkinter.BooleanVar(value=False)
        self.checkbox_lap = tkinter.Checkbutton(self, variable=self.checkbox_lapisOn, onvalue=True, offvalue=False,command=self.lap_acts)
        self.lb_ksize = tkinter.Label(self,text="Розмір ядра",bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.lb_scale = tkinter.Label(self, text="Масштабування", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.lb_delta = tkinter.Label(self, text="Коефіцієнт", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))

        """buttons & enter fields"""
        self.show_camera_btn = tkinter.Button(self,text="Включить камеру", command=self.camera)
        self.off_camera_btn = tkinter.Button(self, text="Выключить камеру", command=self.stop_camera)

        self.min_thresh_entr = tkinter.Entry(self, font=("Helvetica", 12))
        self.max_thresh_entr = tkinter.Entry(self, font=("Helvetica", 12))


        self.ksize_entr = tkinter.Entry(self, font=("Helvetica", 12))
        self.scale_entr = tkinter.Entry(self, font=("Helvetica", 12))
        self.delta_entr = tkinter.Entry(self, font=("Helvetica", 12))

        self.oy_entr=tkinter.Entry(self, font=("Helvetica", 14))

        #placement

        """labels"""

        """original"""
        self.lb_og.place(x = 800, y = 20)
        self.checkbox_OG.place(x = 770, y = 20)

        """gray filter"""
        self.lb_gray.place(x=40, y=20)
        self.checkbox_GRAY.place(x=10, y=20)

        """vertical"""
        self.lb_oy.place(x=40, y=40)
        self.checkbox_oy.place(x=10, y=40)

        """binarization"""
        self.lb_bin.place(x=300, y=20)
        self.checkbox_bin.place(x=270, y=20)

        """laplacian"""

        self.lb_lap.place(x=300, y=40)
        self.checkbox_lap.place(x=270, y=40)

        """buttons & enter fields"""

        self.show_camera_btn.place(x=40, y= 120)
        self.off_camera_btn.place(x=40, y= 160)


    def stop_camera(self):             #Функція повної зупинки та закривання усіх вікон з фільтрами
        self.stop = 1
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()

    def camera(self):                   #Функція активування вікон з перевіркою активності чекбоксів
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():  # Перевірка на існування потоку відеозображення
            messagebox.showerror("Error","Неможливо відкрити камеру")
            return
        self.stop = 0
        if self.checkbox_ogisEnabled.get() == True:
            self.camera_og()
        if self.checkbox_grayisOn.get() == True:
            self.camera_gray()
        if self.checkbox_oyisOn.get() == True:
            self.camera_oy()
        if self.checkbox_binisOn.get() == True:
            self.camera_bin()
        if self.checkbox_lapisOn.get() == True:
            self.camera_lap()

    def camera_og(self):                            #Оригінальне відеозображення без жодного фільтру
        if self.checkbox_ogisEnabled.get() == True:
            ret, frame = self.cap.read()
            cv2.imshow('Original', frame)

            self.after(30, self.camera_og)
        else:
            cv2.destroyWindow('Original')


    def camera_gray(self):                         #Відеозображення у GRAY-просторі
        if self.checkbox_grayisOn.get() == True:
            ret, frame = self.cap.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Переведення зображення у GRAY-простір
            cv2.imshow('GrayColoredFrame', gray_frame)  # Вивід кадру відео на монітор з кольоровим простором GRAY

            self.after(30, self.camera_gray)  # Частота оновлення зображення
        else:
            cv2.destroyWindow('GrayColoredFrame')


    def oy_acts(self):                                    #З'явлення поля для вводу та лейблу при активному чекбоксі у вертикальному зміщенні
        if self.checkbox_oyisOn.get() == True:
            self.oy_entr.place(x=370, y=122)
            self.lb_height_oy.place(x=370, y=100)
        if self.checkbox_oyisOn.get() == False:
            self.oy_entr.place_forget()
            self.lb_height_oy.place_forget()


    def camera_oy(self):                                  #Фільтр вертикального зміщення з перевірками
        if self.checkbox_oyisOn.get() == True:
            try:
                shift_y = float(self.oy_entr.get())
            except ValueError:
                messagebox.showerror("Помилка", "Уведіть число у поле")
                return

            ret, frame = self.cap.read()

            if not ret and self.stop == 0:
                messagebox.showerror("Помилка", "Не вдалося зчитати кадр")
                return


            M = np.float32([[1, 0, 0], [0, 1, shift_y]])
            shifted_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
            cv2.imshow('Shifted', shifted_frame)  # Вивід кадру відео на монітор

            self.after(30, self.camera_oy)  # Частота оновлення зображення
        else:
            cv2.destroyWindow('Shifted')

    def bin_acts(self):                               #З'явлення полей для вводу та лейблів при активному чекбоксі у бінарізації
        if self.checkbox_binisOn.get() == True:
            self.max_thresh_entr.place(x= 530, y = 168, width = 50)
            self.min_thresh_entr.place(x=370, y=168, width = 50)
            self.lb_thresh.place(x=370, y=146)
        if self.checkbox_binisOn.get() == False:
            self.max_thresh_entr.place_forget()
            self.min_thresh_entr.place_forget()
            self.lb_thresh.place_forget()


    def camera_bin(self):                           #Фільтр бінарізації з різними порогами з перевірками
        if self.checkbox_binisOn.get():
            if self.cap.isOpened() and not self.stop:
                ret, frame = self.cap.read()
                try:
                    thresh = int(self.min_thresh_entr.get())  # мінімальний поріг
                    if thresh > 255 or thresh < 0:
                        raise InvalidThresholdError("Яркість повинна входити у межі 0<x<256")
                except ValueError:
                    messagebox.showerror("Помилка", "Уведіть число у поле")
                    return 1

                try:
                    maxvalue = int(self.max_thresh_entr.get())
                    if maxvalue > 255 or maxvalue < 0:
                        raise InvalidThresholdError("Яркість повинна входити у межі 0<x<256")
                except ValueError:
                    messagebox.showerror("Помилка", "Уведіть число у поле")
                    return
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    _, binary = cv2.threshold(gray, thresh, maxvalue, cv2.THRESH_BINARY)
                    cv2.imshow('Binarized', binary)

                self.after(30, self.camera_bin)
            else:
                cv2.destroyWindow('Binarized')


    def lap_acts(self):                         #З'явлення полей для вводу та лейблів при активному чекбоксі у лапласі
        if self.checkbox_lapisOn.get() == True:
            self.lb_ksize.place(x=370, y=188)
            self.lb_scale.place(x=370, y=232)
            self.lb_delta.place(x=370, y=276)
            self.ksize_entr.place(x=370, y=210)
            self.scale_entr.place(x=370, y=254)
            self.delta_entr.place(x=370, y=298)
        if self.checkbox_lapisOn.get() == False:
            self.lb_ksize.place_forget()
            self.lb_scale.place_forget()
            self.lb_delta.place_forget()
            self.ksize_entr.place_forget()
            self.scale_entr.place_forget()
            self.delta_entr.place_forget()


    def camera_lap(self):                       #Фільтр виділення меж зі змінними параметрами з перевірками
        if self.checkbox_lapisOn.get():
            if self.cap.isOpened() and not self.stop:  # Перевірка читання камери
                ret, frame = self.cap.read()  # Читання кадру відео
                try:
                    ksize = int(self.ksize_entr.get())  # розмір ядра
                    if ksize%2 == 0:
                        raise PairedNumber("Розмір ядра має бути непарним!")
                except ValueError:
                    messagebox.showerror("Помилка", "Уведіть число у поле")
                    return 1
                try:
                    scale = int(self.scale_entr.get())  # масштаб
                except ValueError:
                    messagebox.showerror("Помилка", "Уведіть число у поле")
                    return 1
                try:
                    delta = int(self.delta_entr.get())  # контрастність
                except ValueError:
                    messagebox.showerror("Помилка", "Уведіть число у поле")
                    return 1
                laplacian = cv2.Laplacian(
                    frame,
                    ddepth=cv2.CV_64F,  # глибина зображення(64FLOAT)
                    ksize=ksize,
                    scale=scale,
                    delta=delta,
                    borderType=cv2.BORDER_CONSTANT)  # тип обробки
                laplacian_abs = cv2.convertScaleAbs(laplacian)

                cv2.imshow("Laplacian", laplacian_abs)

                self.after(30, self.camera_lap) # Частота оновлення зображення
        else:
            cv2.destroyWindow("Laplacian")


if __name__ == '__main__':
    application = tkinter.Tk()
    Window1(application)
    application.geometry("1024x768+900+500")
    application.title("cw7-322-v01-Shaienko-Vitaliy")
    application.mainloop()                                # Запуск програми
