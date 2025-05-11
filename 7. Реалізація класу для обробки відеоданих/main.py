import cv2
import numpy as np
import tkinter
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

class Window1(tkinter.Frame):
    def __init__(self, parent):
        # settings

        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tkinter.BOTH, expand=1)
        self.config(bg="#000033")
        self.create_widgets()

        self.cap = None
        self.is_camera = tkinter.BooleanVar(value=False)
        self.stop = 0

        #objects
    def create_widgets(self):
        #initialization

        """ORIGINAL"""

        self.lb_og = tkinter.Label(self, text="Орігінальне зображення", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.checkbox_ogisEnabled = tkinter.BooleanVar(value=True)
        self.checkbox_OG = tkinter.Checkbutton(self, state = "disabled", variable = self.checkbox_ogisEnabled)
        self.label_original = tkinter.Label(self)

        """GRAY"""
        self.lb_gray = tkinter.Label(self, text="Фільтр GRAY", bg="#000033", fg="#ADD8E6", font=("Helvetica", 12))
        self.checkbox_grayisOn = tkinter.BooleanVar(value=False)
        self.checkbox_GRAY = tkinter.Checkbutton(self, variable=self.checkbox_grayisOn, onvalue=True, offvalue=False)
        self.label_filtered = tkinter.Label(self)

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
        self.load_video_btn = tkinter.Button(self, text="Відкрити відео", command=self.video)
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

        self.load_video_btn.place(x = 40, y = 80)
        self.show_camera_btn.place(x=40, y= 120)
        self.off_camera_btn.place(x=40, y= 160)


    def stop_camera(self):             #Функція повної зупинки та закривання усіх вікон з фільтрами
        self.stop = 1
        if hasattr(self, '_after_id'):
            self.after_cancel(self._after_id)
        if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.label_original.place_forget()
        self.label_filtered.place_forget()

    def video(self):
        self.stop_camera()
        self.stop = 0
        self.is_camera = False
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if path:
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
            self.cap = cv2.VideoCapture(path)
            self.label_original.place(x=20, y=200, width=400, height=300)
            self.label_filtered.place(x=500, y=200, width=400, height=300)
            self.process_frame()

    def camera(self):                   #Функція активування вікон з перевіркою активності чекбоксів
        self.stop_camera()
        self.stop = 0
        self.is_camera = True
        self.cap = cv2.VideoCapture(0)  
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Неможливо відкрити камеру або відеофайл")
            return
        self.label_original.place(x=20, y=200, width=400, height=300)
        self.label_filtered.place(x=500, y=200, width=400, height=300)
        self.process_frame()


    def process_frame(self):
        if not self.cap.isOpened() or self.stop:
            return

        ret, frame = self.cap.read()
        if not ret:
            if not self.is_camera:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                print(1)
                self.after(30, self.process_frame)
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_original = Image.fromarray(rgb_frame)
        resized_img = pil_original.resize((400, 300),Image.Resampling.LANCZOS)

        filtered = frame.copy()

        #Застосування фільтрів
        try:
            if self.checkbox_grayisOn.get():
                filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

            if self.checkbox_oyisOn.get():
                shift_y = float(self.oy_entr.get())
                M = np.float32([[1, 0, 0], [0, 1, shift_y]])
                filtered = cv2.warpAffine(filtered, M, (filtered.shape[1], filtered.shape[0]))

            if self.checkbox_binisOn.get():
                if not self.min_thresh_entr.get() or not self.max_thresh_entr.get():
                    raise ValueError("Уведіть пороги для бінаризації")
                thresh = int(self.min_thresh_entr.get())
                maxvalue = int(self.max_thresh_entr.get())
                if len(filtered.shape) == 3:
                    filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
                _, filtered = cv2.threshold(filtered, thresh, maxvalue, cv2.THRESH_BINARY)

            if self.checkbox_lapisOn.get():
                ksize = int(self.ksize_entr.get())
                scale = int(self.scale_entr.get())
                delta = int(self.delta_entr.get())
                filtered = cv2.Laplacian(filtered, cv2.CV_64F, ksize=ksize, scale=scale, delta=delta)
                filtered = cv2.convertScaleAbs(filtered)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            self.stop_camera()
            return

        # Відображення оригіналу
        img_original = ImageTk.PhotoImage(resized_img)
        self.label_original.imgtk = img_original
        self.label_original.configure(image=img_original)

        
        if len(filtered.shape) == 2:                                    #Перетворення для фільтрованих відеозображень
            filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
        else:
            filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)
        pil_filtered = Image.fromarray(filtered)
        resized_filtered = pil_filtered.resize((400, 300), Image.Resampling.LANCZOS)

        img_filtered = ImageTk.PhotoImage(resized_filtered)
        self.label_filtered.imgtk = img_filtered
        self.label_filtered.configure(image=img_filtered)

        if hasattr(self, '_after_id'):
            # отменяем предыдущий, чтобы не накапливать
            self.after_cancel(self._after_id)
        self._after_id = self.after(30, self.process_frame)

    def oy_acts(self):                                    #З'явлення поля для вводу та лейблу при активному чекбоксі у вертикальному зміщенні
        if self.checkbox_oyisOn.get() == True:
            self.oy_entr.place(x=170, y=96)
            self.lb_height_oy.place(x=170, y=66)
        if self.checkbox_oyisOn.get() == False:
            self.oy_entr.place_forget()
            self.lb_height_oy.place_forget()

    def bin_acts(self):                               #З'явлення полей для вводу та лейблів при активному чекбоксі у бінарізації
        if self.checkbox_binisOn.get() == True:
            self.max_thresh_entr.place(x= 600, y = 40, width = 50)
            self.min_thresh_entr.place(x=440, y=40, width = 50)
            self.lb_thresh.place(x=400, y=20)
        if self.checkbox_binisOn.get() == False:
            self.max_thresh_entr.place_forget()
            self.min_thresh_entr.place_forget()
            self.lb_thresh.place_forget()


    def lap_acts(self):                         #З'явлення полей для вводу та лейблів при активному чекбоксі у лапласі
        if self.checkbox_lapisOn.get() == True:
            self.lb_ksize.place(x=570, y=68)
            self.lb_scale.place(x=570, y=112)
            self.lb_delta.place(x=570, y=156)
            self.ksize_entr.place(x=570, y=90)
            self.scale_entr.place(x=570, y=134)
            self.delta_entr.place(x=570, y=178)
        if self.checkbox_lapisOn.get() == False:
            self.lb_ksize.place_forget()
            self.lb_scale.place_forget()
            self.lb_delta.place_forget()
            self.ksize_entr.place_forget()
            self.scale_entr.place_forget()
            self.delta_entr.place_forget()


if __name__ == '__main__':
    application = tkinter.Tk()
    Window1(application)
    application.geometry("1024x540+900+500")
    application.title("cw7-322-v01-Shaienko-Vitaliy")
    application.mainloop()                                # Запуск програми
