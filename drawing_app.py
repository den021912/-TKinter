import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.canvas.bind('<Button-3>', self.pick_color) # Обработчик выбора цвета с холста

        """Добавляем гарячие клавиши"""
        self.root.bind('<Control-s>', self.save_image) # для сохранения изображения
        self.root.bind('<Control-c>', self.choose_color) # для выбора цвета

        """Добавление параметра для предварительного просмотра цвета кисти."""
        self.preview_color = tk.Canvas(root, width=40, height=30, background=self.pen_color) # Создаем окошко 40*30, которое показывает текущий цвет
        self.preview_color.pack(side=tk.LEFT)


    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        """Выпадающий список для выбора размера кисти"""
        sizes = [1, 2, 5, 10]
        self.brush_size = tk.IntVar(control_frame)
        self.brush_size.set(sizes[1])
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_scale, *sizes, command = self.update_brush_size)
        brush_size_menu.pack(side = tk.LEFT)

        """Добавляем ластик"""
        self.eraser_get_button = tk.Button(control_frame, text = "Ластик", command = self.eraser_get)
        self.eraser_get_button.pack(side = tk.LEFT)

        """Добавлена кнопка для изменения размера холста"""
        change_canvas_button = tk.Button(control_frame, text = "Изменить размер холста", command = self.change_size_canvas)
        change_canvas_button.pack(side = tk.LEFT)


    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width = self.brush_size_scale.get(), fill = self.pen_color,
                                    capstyle = tk.ROUND, smooth = tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill = self.pen_color,
                           width = self.brush_size_scale.get())
        self.last_x = event.x
        self.last_y = event.y


    def reset(self, event):
        self.last_x, self.last_y = None, None


    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)


    def choose_color(self, event=None):
        """Открывает диалоговое окно выбора цвета."""
        self.pen_color = colorchooser.askcolor(color = self.pen_color)[1]
        self.preview_color.configure(bg = self.pen_color)


    def save_image(self, event=None):
        """Открывает диалоговое окно сохранить изображение, в случае успешного сохранения выводится сообщение об успешном сохранении."""
        file_path = filedialog.asksaveasfilename(filetypes = [('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


    def change_size_canvas(self): # Функция изменения размера холста
        width = tk.simpledialog.askinteger(title = "Изменить размер холста", prompt = "Ширина холста:")
        height = tk.simpledialog.askinteger(title = "Изменить размер холста", prompt = "Высота холста:")
        self.canvas.config(width = width, height = height)
        self.image = self.image.resize((width, height))
        self.draw = ImageDraw.Draw(self.image)


    def update_brush_size(self, size):
        self.brush_size = int(size)


    def eraser_get(self):
        #Метод для работы ластика
        if self.pen_color == "white":
            self.pen_color = self.previous_color
        else:
            # Сохраняем текущий цвет и переключаем на ластик
            self.previous_color = self.pen_color
            self.pen_color = "white"


    def pick_color(self, event): # Функция которая обновляет цвет с холста
        color = self.image.getpixel((event.x, event.y))  # Получаем цвет пикселя
        self.pen_color = '#%02x%02x%02x' % color


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
