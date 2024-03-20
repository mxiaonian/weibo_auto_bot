# -*- coding: utf-8 -*-
import json
import random
import sqlite3
import threading
import time
from tkinter import messagebox
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from DrissionPage.errors import ElementNotFoundError
from data import Data
from login import Login
from methods import MyMethods
from notice import Notice


def update_progress_text(percentage, progress_text):
    formatted_percentage = "{:.4f}%".format(percentage)
    progress_text.set(f"已完成{formatted_percentage}")


def init_bower_set():
    """初始化浏览器"""
    options = ChromiumOptions()
    options.set_timeouts(30)
    options.set_browser_path(r'.\chrome\chrome.exe')
    options.set_local_port(9888)
    options.set_argument("--disable-notifications")
    options.set_argument("--window-size=1920,2000")
    options.set_argument("--force-device-scale-factor=1")
    page = ChromiumPage(options)
    return page


class Interactive:
    def __init__(self):
        self.methods = MyMethods()
        self.data = Data()
        self.notice = Notice()
        self.login = Login()

    def start_interactive_button_click(self, window, progress_bar, user_start_index, interactive_num, progress_text):
        """
        开始互动
        - window: 所在的gui界面
        - progress_bar: 要更新的进度条
        - start_index: 开始互动的序号
        - like_ande_comments_number: 要互动的次数
        """
        # 创建一个线程来执行耗时的操作
        thread = threading.Thread(target=self.start_interactive,
                                  args=(window, progress_bar, user_start_index, interactive_num, progress_text),
                                  daemon=True)
        thread.start()

    def start_interactive(self, window, progress_bar, user_start_index, interactive_num, progress_text):
        """
        开始互动
        - window: 所在的gui界面
        - progress_bar: 要更新的进度条
        - start_index: 开始互动的序号
        - like_ande_comments_number: 要互动的次数
        """
        self.check_login()
        page = init_bower_set()
        page.get("https://weibo.com")
        with open('data/cookies.json', 'r') as f:
            cookies = json.load(f)
        page.set.cookies(cookies)
        page.refresh()
        # 链接数据库
        self.notice.log_message(f"正在链接数据库...")
        conn = sqlite3.connect('data/interactive_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 用户名, 用户ID FROM interactive_list;")
        data = cursor.fetchall()
        self.notice.log_message(f"数据库链接成功...")
        user_start_index = int(user_start_index)
        progress_magnification = int(interactive_num)
        original_progress = len(data[user_start_index - 1:])
        # 设置进度条的最大值
        progress_bar["maximum"] = progress_magnification * original_progress
        user_index = user_start_index
        # 遍历数据，从指定索引开始
        for i in range(user_start_index - 1, len(data)):
            row = data[i]
            user_name = row[0]
            user_id = row[1]

            page.get(f"https://weibo.com/{user_id}")
            self.notice.log_message(f"正在访问第【{user_index}】个微博用户，微博名【 {user_name} 】的主页...")

            end_index = int(interactive_num)
            data_index = 0
            do_like_count = 0  # 计数器，记录 do_like 的次数
            while True:
                item = page.ele(f'@data-index={data_index}')
                if item:
                    page.scroll.to_see(item, center=True)
                    # 高亮显示帖子
                    self.methods.highlight_element(page, item)
                    do_name = self.get_name(user_name, item)
                    # 针对原创微博进行操作
                    if do_name == 0:
                        time.sleep(2)
                        # 滚动至帖子可见位置
                        self.do_like(page, item)
                        self.do_comment(page, item)
                        do_like_count += 1
                        self.notice.log_message(f"点赞并评论【 {user_name} 】的第【 {do_like_count} 】条微博成功")
                        # 更新GUI中的进度条
                        progress_value = (i - (user_start_index - 1)) / (len(data) - user_start_index + 1)
                        progress_bar["value"] = progress_value * 100  # 假设进度条最大值为100
                        update_progress_text(progress_value * 100, progress_text)
                        window.update()

                        time.sleep(random.uniform(5, 10))
                    # 针对转发的微博进行操作
                    elif do_name == 1:
                        time.sleep(2)
                        self.do_relay_like(page, item)
                        self.do_relay_comment(page, item)
                        do_like_count += 1
                        self.notice.log_message(f"点赞并评论【 {user_name} 】的第【 {do_like_count} 】条微博成功")
                        # 更新GUI中的进度条
                        progress_value = (i - (user_start_index - 1)) / (len(data) - user_start_index + 1)
                        progress_bar["value"] = progress_value * 100  # 假设进度条最大值为100
                        update_progress_text(progress_value * 100, progress_text)
                        window.update()

                        time.sleep(random.uniform(5, 10))
                    # 针对系统推荐的微博进行操作
                    elif do_name == 2:
                        pass
                    else:
                        pass
                    self.methods.remove_highlight(page, item)
                    data_index += 1

                if do_like_count >= end_index:
                    break
            self.notice.log_message(f"为 【{user_name}】点赞论结束,共点赞评论【  {do_like_count} 】个帖子")
            user_index += 1
        update_progress_text(100.0000, progress_text)
        window.update()
        messagebox.showinfo("成功", "所有用户互动已完成")

    def check_login(self):
        """判断是否登录"""
        if self.login.check_cookies_file():
            pass
        else:
            messagebox.showinfo("错误", "未找到登录信息，请先登录")

    def do_like(self, page, item):
        """执行点赞
        :param page: 浏览器驱动
        :param item: 传入需点赞的帖子
        """
        like_button = item.ele('.woo-like-iconWrap')
        self.methods.highlight_element(page, like_button)
        like_button.click()
        time.sleep(2)
        self.methods.remove_highlight(page, like_button)

    def do_relay_like(self, page, item):
        """执行转发点赞
        :param page: 浏览器驱动
        :param item: 传入需转发点赞的帖子
        """
        relay_like_buttons = item.eles(".woo-like-iconWrap")
        relay_like_button = relay_like_buttons[1]
        self.methods.highlight_element(page, relay_like_button)
        relay_like_button.click()
        time.sleep(2)
        self.methods.remove_highlight(page, relay_like_button)

    def get_name(self, name, item):
        """内部函数，获取用户名称,判断微博为原创、转发、系统推荐、系统推荐转发
           : 返回值为0则为原创微博
           ：返回值为1则为转发微博
           ：返回值为2则为系统推荐微博
           ：返回值为3则为系统推荐的转发微博
        """
        try:
            elements = item.eles(".ALink_default_2ibt1")
            # 获取第一个元素的aria-label属性值
            first_aria_label = elements[0].attr("aria-label")
            if len(elements) > 1:
                # 检查第一个aria-label是否为name
                if first_aria_label == name:
                    self.notice.log_message(f"此条微博为【 {name} 】转发的微博")
                    return 1
                else:
                    self.notice.log_message("此条微博为系统推荐的转发微博，跳过")
                    return 3
            elif len(elements) == 1:
                if first_aria_label == name:
                    # self.log_message("此条微博为原创微博，进行点赞评论操作")
                    return 0
                else:
                    self.notice.log_message("此条微博为推荐的微博，跳过")
                    return 2
            else:
                # 如果没有找到元素，也返回None
                self.notice.log_message('未找到此条发送微博的用户名')
                return None
        except ElementNotFoundError:
            # 处理元素未找到的异常
            self.notice.log_message('未找到元素')
            return None

    def do_comment(self, page, item):
        """执行评论
        :param page:传入浏览器驱动
        :param item:传入需评论的帖子
        """
        comment_button = item.ele(".woo-font woo-font--comment toolbar_commentIcon_3o7HB")
        self.methods.highlight_element(page, comment_button)
        comment_button.click()
        time.sleep(3)
        comment_box = item.ele('.Form_input_3JT2Q')
        comment = self.data.get_random_comments()
        comment_box.input(comment)
        time.sleep(1)
        do_comment_button = item.ele('.woo-button-content')
        do_comment_button.click()
        time.sleep(3)
        comment_button.click()
        self.methods.remove_highlight(page, comment_button)

    def do_relay_comment(self, page, item):
        """执行评论【完成】
        :param page: 传入浏览器驱动
        :param item:传入需评论的帖子
        """
        relay_comment_buttons = item.eles(".woo-font woo-font--comment toolbar_commentIcon_3o7HB")
        relay_comment_button = relay_comment_buttons[1]
        self.methods.highlight_element(page, relay_comment_button)
        relay_comment_button.click()
        time.sleep(3)
        comment_box = item.ele('.Form_input_3JT2Q')
        comment = self.data.get_random_comments()
        comment_box.input(comment)
        time.sleep(1)
        do_comment_button = item.ele('.woo-button-content')
        do_comment_button.click()
        time.sleep(3)
        relay_comment_button.click()
        self.methods.remove_highlight(page, relay_comment_button)

    def like_and_comment(self, page, interactive_num, name):
        """
        自动点赞评论微博页面上的帖子
        参数:
        :param name: 浏览器驱动
        :param interactive_num: 互动次数
        :param page: 互动的用户名
        """
        self.notice.log_message("开始自动点赞评论...")
        end_index = int(interactive_num)
        data_index = 0
        do_like_count = 0  # 计数器，记录 do_like 的次数
        while True:
            item = page.ele(f'@data-index={data_index}')
            if item:
                page.scroll.to_see(item, center=True)
                # 高亮显示帖子
                self.methods.highlight_element(page, item)
                do_name = self.get_name(name, item)
                # 针对原创微博进行操作
                if do_name == 0:
                    time.sleep(2)
                    # 滚动至帖子可见位置
                    self.do_like(page, item)
                    self.do_comment(page, item)
                    do_like_count += 1
                    self.notice.log_message(f"点赞并评论【 {name} 】的第【 {do_like_count} 】条微博成功")
                    time.sleep(2)
                # 针对转发的微博进行操作
                elif do_name == 1:
                    time.sleep(2)
                    self.do_relay_like(page, item)
                    self.do_relay_comment(page, item)
                    do_like_count += 1
                    self.notice.log_message(f"点赞并评论【 {name} 】的第【 {do_like_count} 】条微博成功")
                    time.sleep(2)
                # 针对系统推荐的微博进行操作
                elif do_name == 2:
                    pass
                else:
                    pass
                time.sleep(random.uniform(5, 10))
                self.methods.remove_highlight(page, item)
                data_index += 1
            if do_like_count >= end_index:
                break
        self.notice.log_message(f"为 【{name}】点赞论结束,共点赞评论【  {do_like_count} 】个帖子")
