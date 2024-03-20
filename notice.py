# -*- coding: utf-8 -*-
from methods import MyMethods
import os
import datetime
import threading
import tkinter as tk
import logging
"""通知操作类函数"""


class Notice:
    def __init__(self):
        self.massage_log_end_line = 0
        self.end_line = 0
        self.methods = MyMethods()
        self.interactive_logger = logging.getLogger('interactive')
        self.interactive_logger.setLevel(logging.INFO)
        self.message_logger = logging.getLogger('message')
        self.message_logger.setLevel(logging.INFO)

    @staticmethod
    def add_run_info(status_bar, message):
        """
        :param status_bar:传入的状态栏
        :param message: 状态栏显示的文字
        """
        status_bar.config(text=message)

    def log_message(self, message):
        today = datetime.date.today().strftime('%Y-%m-%d')
        log_folder = 'log'
        filename = os.path.join(log_folder, f"log-{today}.txt")
        handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.interactive_logger.handlers:
            self.interactive_logger.addHandler(handler)
        self.interactive_logger.info(message)

    def send_message_log(self, message):
        today = datetime.date.today().strftime('%Y-%m-%d')
        log_folder = 'log'
        massage_filename = os.path.join(log_folder, f"massage-log-{today}.txt")
        handler = logging.FileHandler(massage_filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.message_logger.handlers:
            self.message_logger.addHandler(handler)
        self.message_logger.info(message)

    def show_log(self, text_box, root):
        # 判断是否滚动到最底部
        scrollbar_at_bottom = text_box.yview()[1] == 1.0
        today = datetime.date.today().strftime('%Y-%m-%d')
        # 检查文件是否存在
        log_folder = 'log'
        log_filename = os.path.join(log_folder, f'log-{today}.txt')
        if self.end_line == 0 and os.path.exists(log_filename):
            # 如果self.end_line为0且日志文件存在，则先将已存在的日志文件加载到文本框中
            with open(log_filename, 'r') as file:
                log_content = file.readlines()
            for line in log_content:
                text_box.insert(tk.END, line)
            # 设置self.end_line为日志文件的行数
            self.end_line = len(log_content)
        if self.end_line > 0:
            # 获取新增的日志行
            with open(log_filename, 'r') as file:
                log_content = file.readlines()
            add_log = log_content[self.end_line:]
            if add_log:
                # 将新增的日志行插入到文本框中
                for line in add_log[::1]:  # 顺序遍历新增的日志行
                    text_box.insert(tk.END, line)  # 从底部插入新的日志内容
                # 更新end_line索引
                self.end_line = len(log_content)
                # 判断是否滚动到最底部
                if scrollbar_at_bottom:
                    # 将scrollbar滚动到文本框的end_line
                    text_box.see(tk.END)
        # 定时调用show_log函数
        root.after(1000, self.show_log, text_box, root)

    # 在GUI类中添加一个新的方法，用于启动日志更新线程
    def start_log_update_thread(self, send_massage_text_box, root):
        log_update_thread = threading.Thread(target=self.show_send_massage_log,
                                             args=(send_massage_text_box, root,))
        log_update_thread.daemon = True  # 设置线程为守护线程，主线程退出时自动退出
        log_update_thread.start()

    def show_send_massage_log(self, send_massage_text_box, root):
        # 判断是否滚动到最底部
        scrollbar_at_bottom = send_massage_text_box.yview()[1] == 1.0
        today = datetime.date.today().strftime('%Y-%m-%d')
        # 检查文件是否存在
        log_folder = 'log'
        massage_log_filename = os.path.join(log_folder, f'massage-log-{today}.txt')
        if self.massage_log_end_line == 0 and os.path.exists(massage_log_filename):
            # 如果self.end_line为0且日志文件存在，则先将已存在的日志文件加载到文本框中
            with open(massage_log_filename, 'r') as file:
                massage_log_content = file.readlines()
            for line in massage_log_content:
                send_massage_text_box.insert(tk.END, line)
            # 设置self.end_line为日志文件的行数
            self.massage_log_end_line = len(massage_log_content)
        if self.massage_log_end_line > 0:
            # 获取新增的日志行
            with open(massage_log_filename, 'r') as file:
                massage_log_content = file.readlines()
            add_massage_log = massage_log_content[self.massage_log_end_line:]
            if add_massage_log:
                # 将新增的日志行插入到文本框中
                for line in add_massage_log[::1]:  # 顺序遍历新增的日志行
                    send_massage_text_box.insert(tk.END, line)  # 从底部插入新的日志内容
                # 更新end_line索引
                self.massage_log_end_line = len(massage_log_content)
                # 判断是否滚动到最底部
                if scrollbar_at_bottom:
                    # 将scrollbar滚动到文本框的end_line
                    send_massage_text_box.see(tk.END)
        # 定时调用show_log函数
        root.after(1000, self.show_send_massage_log, send_massage_text_box, root)
