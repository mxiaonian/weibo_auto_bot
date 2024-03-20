# -*- coding: utf-8 -*-
import os
from tkinter import *
import cv2
from PIL import Image, ImageTk
import time
import tkinter as tk

from moviepy.video.io.VideoFileClip import VideoFileClip


class MyMethods:
    def __init__(self):
        self.video_screenshot = []
        self.videos = []
        self.photos = []

    def highlight_element(self, page, element):
        """
        高亮显示某指定元素
        :param page:传入的浏览器驱动
        :param element:指定高亮显示的某元素
        """
        highlight_style = "border: 1px solid red;"
        page.run_js("arguments[0].setAttribute('style', arguments[1]);", element, highlight_style)

    def remove_highlight(self, page, element):
        """
        移除指定元素的高亮显示
        :param page:传入的浏览器驱动
        :param element:移除高亮显示的某元素
        """
        page.run_js("arguments[0].removeAttribute('style');", element)

    def get_item_content(self, item):
        """内部函数,获取指定元素的文字内容"""
        # 如果找到展开按钮，则点击展开按钮，并等待2秒后再获取文字内容
        if item.ele('.expand'):
            item.ele('.expand').click()
            time.sleep(2)
            item_text = item.ele('.detail_wbtext_4CRf9').text
            return item_text
        else:
            item_text = item.ele('.detail_wbtext_4CRf9').text
            return item_text

    def traverse_and_collect_txt_files(self, directory):
        text_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".txt"):
                    text_files.append(os.path.join(root, file))

        return text_files

    def traverse_and_collect_images(self, directory):
        image_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_files.append(os.path.join(root, file))
        return image_files

    def traverse_and_collect_videos(self, directory):
        videos_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".mp4"):
                    videos_files.append(os.path.join(root, file))
        return videos_files

    def load_txt_file(self, scrollable_frame):
        directory = "./data"
        text_files = self.traverse_and_collect_txt_files(directory)
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
                text_widget.bind("<Double-1>", lambda e: self.open_new_window(text, text_file))

    def open_new_window(self, text, text_file_path):
        # 创建主窗口
        new_window = tk.Toplevel()
        # 设置主窗口大小
        new_window.geometry("650x480")
        new_window.title("详细内容")
        # 显示文字
        frame2 = tk.Frame(new_window)
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
        # get photos for the current text file
        self.get_photo(os.path.dirname(text_file_path))
        print(self.photos)
        if self.photos:  # 检查 self.photos 是否为空
            image_frame = tk.Frame(new_window)
            image_frame.pack(fill=X, side=TOP)
            for i, photo in enumerate(self.photos):
                row = i // 3  # 计算行
                column = i % 3  # 计算列
                photo_canvas = tk.Canvas(image_frame, height=100, width=100)
                photo_canvas.grid(row=row, column=column, padx=5, pady=5)
                image_id = photo_canvas.create_image(50, 50, image=photo,
                                                     anchor="center")  # 将图像的 x 和 y 坐标设置为图像的宽度和高度的一半
                photo_canvas.tag_bind(image_id, "<Double-1>",
                                      lambda e, filepath=photo.filepath: self.open_file(filepath))  # 为图像绑定双击事件

        if self.video_screenshot:
            video_frame = tk.Frame(new_window)
            video_frame.pack(fill=X, side=TOP)
            for i, frame in enumerate(self.video_screenshot):
                video_canvas = tk.Canvas(video_frame)
                video_canvas.pack(fill=X, side=TOP)
                video_id = video_canvas.create_image(0, 0, image=frame, anchor="center")
                video_canvas.tag_bind(video_id, "<Double-1>",
                                      lambda e, filepath=frame.filepath: self.open_file(filepath))  # 为视频截图绑定双击事件

    def get_photo(self, directory):
        image_files = self.traverse_and_collect_images(directory)
        self.photos = []
        for image in image_files:
            img = Image.open(image)
            width, height = img.size
            crop_height = width
            img = img.crop((0, 0, width, crop_height))
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            photo.filepath = image  # 保存图片的路径
            self.photos.append(photo)
        return self.photos

    def get_video_screenshot(self):
        videos_files = self.traverse_and_collect_videos("./data")
        self.video_screenshot = []
        for video in videos_files:
            load_video = cv2.VideoCapture(video)
            total_frames = int(load_video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = load_video.get(cv2.CAP_PROP_FPS)
            target_frame = int(total_frames * 2 / 3)
            load_video.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = load_video.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(image=frame)
            frame.filepath = video  # 保存视频文件的路径
            self.video_screenshot.append(frame)
        return self.video_screenshot

    def open_file(self, filepath):
        os.startfile(filepath)  # 使用系统默认的程序打开图片
