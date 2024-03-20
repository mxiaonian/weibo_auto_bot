# -*- coding: utf-8 -*-
import json
import os
import threading
import time
from tkinter import messagebox
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from PIL import Image, ImageTk
from notice import Notice


class Login:
    def __init__(self):
        self.remove_qrimage()
        self.notice = Notice()

    def login_weibo_click(self, photo_label, login_status_bar):
        # 创建一个线程来执行耗时的操作
        login_thread = threading.Thread(target=self.login_weibo, args=(photo_label, login_status_bar,), daemon=True)
        login_thread.daemon = True
        login_thread.start()

    def add_login_image(self, photo_label):
        image_path = 'data/qr_image.jpg'
        # 创建一个新的线程来检测文件是否存在
        stop_event = threading.Event()
        threading.Thread(target=self.check_image_exists, args=(image_path, photo_label, stop_event)).start()

    @staticmethod
    def check_image_exists(image_path, photo_label, stop_event):
        # 检测文件是否存在，如果不存在则等待一秒钟后重新检测
        while not os.path.exists(image_path):
            time.sleep(1)
            # 检查是否需要停止检测
            if stop_event.is_set():
                return
        # 如果文件存在，则执行显示图片的逻辑
        if os.path.exists(image_path):
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            photo_label.configure(image=photo)
            photo_label.image = photo
            photo_label.update()
        print('已存在二维码')

    @staticmethod
    def remove_qrimage():
        for file_name in os.listdir('data'):
            if file_name.startswith('qr_image') and file_name.endswith('.jpg'):
                os.remove(os.path.join('data', file_name))
            else:
                pass

    def login_weibo(self, photo_label, login_status_bar):
        self.remove_qrimage()
        # 初始化浏览器
        options = ChromiumOptions()
        options.set_timeouts(30)
        options.set_browser_path(r'.\chrome\chrome.exe')
        options.set_local_port(9888)
        options.set_argument("--disable-notifications")
        options.set_argument("--window-size=1920,2000")
        options.set_argument("--force-device-scale-factor=1")
        # options.headless(True)
        page = ChromiumPage(options)
        page.get("https://weibo.com/newlogin")
        if "https://weibo.com/newlogin" in page.url:
            self.notice.add_run_info(login_status_bar, "正在获取登录二维码中，请稍后...")
            load_button = page.ele('.LoginCard_text_3BtVI')
            load_button.click()
            load_qr_image = page.ele('.LoginPop_mabox_3Lyr6')
            time.sleep(3)
            load_qr_image.get_screenshot(name='qr_image.jpg', path='data/')
            photo = ImageTk.PhotoImage(Image.open('data/qr_image.jpg'))
            photo_label.configure(image=photo)
            photo_label.image = photo
            photo_label.update()
            self.notice.add_run_info(login_status_bar, "获取二维码成功，请在1分钟内扫描二维码")
            self.wait_login(page=page, time_out=180)
            # 等待 发送 的元素加载完成
            page.wait.ele_loaded('.Tool_checkc_7h2O5')
            cookies = page.cookies(all_info=True)
            self.write_cookies(cookies)
            self.notice.add_run_info(login_status_bar, "登录成功")
            messagebox.showinfo("成功", "登录成功")
        else:
            self.notice.add_run_info(login_status_bar, "已登录")
            messagebox.showinfo("成功", "已登录")

    @staticmethod
    def is_login():
        page = ChromiumPage()
        page.set.window.hide()
        page.get("https://weibo.com/")
        page.wait.doc_loaded()
        if "https://weibo.com/newlogin" in page.url:
            page.quit()
            return False
        else:
            page.quit()
            return True

    @staticmethod
    def wait_login(page, time_out):
        current_url = page.url
        # 记录开始等待的时间
        start_time = time.time()

        # 不断检查当前网址是否发生变化，直到超时或者网址变化
        while current_url == page.url:
            if time.time() - start_time > time_out:
                break
            time.sleep(1)

    @staticmethod
    def read_cookies():
        with open('data/cookies.json', 'r') as f:
            cookies = json.load(f)
            return cookies

    @staticmethod
    def write_cookies(cookies):
        with open('data/cookies.json', 'w') as f:
            json.dump(cookies, f)
        messagebox.showinfo("成功", "已更新登录信息")

    @staticmethod
    def check_cookies_file():
        if os.path.isfile("data/cookies.json"):
            return True
        else:
            return False
