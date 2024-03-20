# -*- coding: utf-8 -*-
import os
import glob
from tkinter import *
import cv2
from PIL import Image, ImageTk
import tkinter as tk

photo_lists = []


def load_data(scrollable_frame):
    # 获取所有以'./data/'开头的文件夹路径
    folders = glob.glob('./data/*')

    # 遍历每个文件夹路径
    for folder in folders:
        # 检查路径是否为文件夹
        if os.path.isdir(folder):
            # 调用load_folder函数加载文件夹内容到scrollable_frame中
            load_folder(folder, scrollable_frame)


def load_folder(folder, scrollable_frame):
    files = glob.glob(f'{folder}/*')
    text_files = [f for f in files if f.endswith('.txt')]
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_file_names = [os.path.basename(f) for f in image_files]
    print(f'load_folder{image_file_names}')
    # 显示文本
    for text_file in text_files:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
            frame = Frame(scrollable_frame)
            frame.pack(fill=X)
            # 创建复选框
            var = IntVar()
            checkbutton = Checkbutton(frame, variable=var)
            checkbutton.pack(side=LEFT)
            # 创建Text部件
            text_widget = Text(frame, height=4, wrap='word', )
            text_widget.pack(side=LEFT, fill=X, padx=10, pady=10)
            # 创建Scrollbar部件，并与Text部件关联
            scrollbar = Scrollbar(frame, command=text_widget.yview, width=0)
            scrollbar.pack(side=LEFT, fill=Y)
            # 将Text部件的滚动命令设置为Scrollbar部件的set方法
            text_widget['yscrollcommand'] = scrollbar.set
            # 在Text部件中显示文本
            text_widget.insert('1.0', text)
            # 绑定双击事件
            text_widget.bind("<Double-1>", lambda e: open_new_window(text, image_files))


def get_photo(image_files):
    global photo_lists
    for image in image_files:
        img = Image.open(image)
        width, height = img.size
        crop_height = width
        img = img.crop((0, 0, width, crop_height))
        img = img.resize((100, 100))  # 调整图片大小
        photo = ImageTk.PhotoImage(img)
        photo_lists.append(photo)
    return photo_lists


def open_new_window(text, image_files):
    # 创建主窗口
    root = tk.Tk()
    # 设置主窗口大小
    root.geometry("650x480")
    root.title("详细内容")
    # 显示文字
    frame2 = tk.Frame(root)
    frame2.pack(fill=X, side=TOP)
    text_frame = Frame(frame2)
    text_frame.pack(fill=X, side=TOP)
    text_widget_1 = tk.Text(text_frame, wrap=tk.WORD, height=5)
    text_widget_1.pack(fill=tk.BOTH, expand=True)
    text_widget_1.insert(tk.END, text)
    # 创建Scrollbar部件，并与Text部件关联
    scrollbar2 = Scrollbar(frame2, command=text_widget_1.yview, width=0)
    scrollbar2.pack(side=LEFT, fill=Y)
    text_widget_1['yscrollcommand'] = scrollbar2.set

    image_frame = tk.Frame(root)
    image_frame.pack(fill=X, side=TOP, pady=10)
    get_photo(image_files)
    photos = photo_lists
    # 在 Frame 中创建多个 Label 来显示图片
    for photo in photos:
        photo_label = tk.Label(image_frame, image=photo)
        photo_label.pack(side=LEFT, fill=X, padx=5, pady=5)
    root.mainloop()
