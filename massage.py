# -*- coding: utf-8 -*-
import json
import sqlite3
import threading
import time
from tkinter import messagebox
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
from DrissionPage.common import Keys
from tqdm import tqdm
from login import Login
from methods import MyMethods
from notice import Notice





def init_massage_bower_set():
    # 创建浏览器，并进入用户首页
    options = ChromiumOptions()
    options.set_timeouts(30)
    options.set_browser_path(r'.\chrome\chrome.exe')
    options.set_local_port(9888)
    options.set_argument("--disable-notifications")
    options.set_argument("--window-size=1920,2000")
    options.set_argument("--force-device-scale-factor=1")
    page = ChromiumPage(options)
    with open('data/cookies.json', 'r') as f:
        cookies = json.load(f)
    page.set.cookies(cookies)
    page.refresh()
    return page


class Massage:
    def __init__(self):
        self.current_progress_text = ""
        self.login = Login()
        self.notice = Notice()
        self.methods = MyMethods()

    def update_massage_progress_text(self, percentage, progress_text):

        formatted_percentage = "{:.4f}%".format(percentage)
        self.current_progress_text = f"已完成{formatted_percentage}"
        progress_text.set(self.current_progress_text)

    def check_massage_login(self):
        page = init_massage_bower_set()
        find_popup = page.ele('.confirmbtn')
        if find_popup:
            find_popup.click()
        else:
            pass

        find_qr_code = page.ele('.qrcode_img')
        if find_qr_code:
            self.login.remove_qrimage()
            find_qr_code.get_screenshot(name='qr_image.jpg', path='data/')
            messagebox.showinfo("未登录", "请在1分钟内打开登录页面扫描二维码登录")
            self.login.wait_login(page, 180)
            cookies = page.cookies(all_info=True)
            self.login.write_cookies(cookies)
        else:
            pass

    def send_massage_button_click(self, window, progress_bar, start_index, send_quantity, message_data, progress_text):
        # 创建一个线程来执行耗时的操作
        send_massage_thread = threading.Thread(target=self.send_messages,
                                               args=(window, progress_bar, start_index, send_quantity, message_data,
                                                     progress_text))
        send_massage_thread.daemon = True  # 设置线程为守护线程，主线程退出时自动退出
        send_massage_thread.start()

    def send_messages(self, window, progress_bar, start_index, send_quantity, message_data, progress_text):

        page = init_massage_bower_set()
        ac = Actions(page)
        page.get("https://api.weibo.com/chat#/chat")
        self.check_massage_login()
        # 查找搜索框元素
        search_box = page.ele('.searchInput flex-1')
        # 连接数据库
        conn = sqlite3.connect('data/interactive_list.db')
        cursor = conn.cursor()
        # 查询用户配置数据
        cursor.execute("SELECT 用户名, 用户ID FROM interactive_list;")
        data = cursor.fetchall()
        # 获取用户输入
        start_index_int = int(start_index)
        send_quantity_int = int(send_quantity)
        user_index_num = start_index_int
        # 设置进度条的最大值
        original_massage_progress = len(data[start_index_int - 1:])
        progress_bar["maximum"] = send_quantity_int * original_massage_progress
        # 执行脚本
        for index, user in enumerate(data[start_index_int - 1:], start=start_index_int):
            name = user[0]
            search_box.input(name)
            time.sleep(1)
            do_user = page.ele(name)
            if do_user:
                do_user.click()
                time.sleep(1)
                for i in range(send_quantity_int):
                    input_box = page.ele('#webchat-textarea')
                    input_box.input(message_data)
                    ac.type(Keys.ENTER)
                    self.notice.send_message_log(f"发送私信到第【 {user_index_num} 】个用户【 {name} 】成功")
                    # 更新进度条的值
                    progress_value = index - start_index_int + 1
                    progress_bar["value"] = progress_value
                    # 计算并更新进度文本
                    percentage = (progress_value / original_massage_progress) * 100
                    self.update_massage_progress_text(percentage, progress_text)
                    # 更新GUI界面
                    window.update()
                    time.sleep(2)
                user_index_num += 1
            else:
                self.notice.send_message_log(f"【发送私信到【 {name} 】失败，该用户不在聊天列表中】")
        self.update_massage_progress_text(100.0000, progress_text)
        # 显示完成消息
        messagebox.showinfo("完成", "消息发送完成")
