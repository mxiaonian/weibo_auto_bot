# -*- coding: utf-8 -*-
import os
import glob
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip


class App:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.canvas = Canvas(self.frame)
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame.pack(fill=BOTH, expand=1)
        self.canvas.pack(side="left", fill=BOTH, expand=1)
        self.scrollbar.pack(side="right", fill="y")

        self.load_data()

    def load_data(self):
        folders = glob.glob('./data/*')
        for folder in folders:
            if os.path.isdir(folder):
                self.load_folder(folder)

    def load_folder(self, folder):
        files = glob.glob(f'{folder}/*')
        text_files = [f for f in files if f.endswith('.txt')]

        # Display text
        for text_file in text_files:
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()
                self.display_text(text, folder)

    def display_text(self, text, folder):
        # Create a new frame for each text
        frame = Frame(self.scrollable_frame)
        frame.pack(fill=X)

        # 创建复选框
        var = IntVar()
        checkbutton = Checkbutton(frame, variable=var)
        checkbutton.pack(side=LEFT)

        # 创建Text部件
        text_widget = Text(frame, width=50, height=4, wrap='word')
        text_widget.pack(side=LEFT, padx=10, pady=10)

        # 创建Scrollbar部件，并与Text部件关联
        scrollbar = Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=LEFT, fill=Y)

        # 将Text部件的滚动命令设置为Scrollbar部件的set方法
        text_widget['yscrollcommand'] = scrollbar.set

        # 在Text部件中显示文本
        text_widget.insert('1.0', text)

        # Bind double click event
        text_widget.bind("<Double-1>", lambda e: self.open_new_window(text, folder))

    def open_new_window(self, text, folder):
        new_window = Toplevel(self.root)
        new_window.title(folder)

        # Display text
        text_label = Label(new_window, text=text)
        text_label.pack()

        # Display images
        image_files = glob.glob(f'{folder}/*')
        image_files = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg'))]
        for image_file in image_files:
            image = Image.open(image_file)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(new_window, image=photo)
            image_label.image = photo  # keep a reference to the image
            image_label.pack()

        # Display videos
        video_files = glob.glob(f'{folder}/*')
        video_files = [f for f in video_files if f.endswith('.mp4')]
        for video_file in video_files:
            clip = VideoFileClip(video_file)
            clip.preview()


root = Tk()
app = App(root)
root.mainloop()
