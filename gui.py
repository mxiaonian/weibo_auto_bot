import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import gather
from data import Data
from interactive import Interactive
from login import Login
from massage import Massage
from methods import MyMethods
from notice import Notice


class Weibo_bot_GUI:
    def __init__(self, root):
        self.massage_progress_text = None
        self.progress_text = None
        self.interactive_start_input_box = None
        self.photo_label = None
        self.interactive_number_input_box = None
        self.send_massage_text_box = None
        self.log_text_box = None
        self.login_status_bar = None
        self.delete_comments_data_input_box = None
        self.message_entry = None
        self.send_quantity_entry = None
        self.start_index_entry = None
        self.comment_number_input_box = None
        self.ID_input_box = None
        self.username_input_box = None
        self.comment_input_box = None
        self.selected_number = None
        self.methods = MyMethods()
        self.login = Login()
        self.massage = Massage()
        self.notice = Notice()
        self.data = Data()
        self.interactive = Interactive()
        self.root = root
        # 初始化 GUI
        self.init_gui()
        self.login.add_login_image(photo_label=self.photo_label)

    def init_gui(self):
        # 放置GUI代码的地方
        # 创建Notebook组件
        notebook = ttk.Notebook(self.root)

        # ——————————————登录标签页—————————————— #
        page1 = ttk.Frame(notebook)
        notebook.add(page1, text="登录")
        # 创建Frame组件
        page1_frame1 = tk.Frame(page1)
        page1_frame1.pack(expand=True)
        # 将内容居中
        page1_frame1.grid_rowconfigure(0, weight=1)
        page1_frame1.grid_columnconfigure(0, weight=1)

        # 创建状态栏标签
        self.login_status_bar = tk.Label(page1, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.login_status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.notice.add_run_info(status_bar=self.login_status_bar, message="欢迎使用小念的微博自动机器人")

        # 在page1_frame1中创建label组件
        self.photo_label = tk.Label(page1_frame1)
        self.photo_label.pack(anchor=tk.CENTER)

        page1_frame2 = tk.Frame(page1)
        page1_frame2.pack(pady=10)
        # 创建登录按钮，调用登录逻辑运行
        login_button = tk.Button(page1_frame2, text="点击登录",
                                 command=lambda: self.login.login_weibo_click(photo_label=self.photo_label,
                                                                              login_status_bar=self.login_status_bar))
        login_button.pack(pady=10)

        # ——————————————自动点赞评论标签页—————————————— #
        page2 = ttk.Frame(notebook)
        notebook.add(page2, text="自动点赞评论")

        page2_frame1 = tk.Frame(page2)
        page2_frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        self.log_text_box = ScrolledText(page2_frame1, width=900, height=20)
        self.log_text_box.pack()
        self.notice.show_log(text_box=self.log_text_box, root=self.root)

        page2_frame4 = tk.Frame(page2)
        page2_frame4.pack(side=tk.TOP, fill=tk.X)
        # 添加进度条
        progress_label = tk.Label(page2_frame4, text="互动进度: ")
        progress_label.pack(side=tk.LEFT, pady=5)
        interactive_progress_bar = ttk.Progressbar(page2_frame4, orient="horizontal", length=450, mode="determinate")
        interactive_progress_bar.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        self.progress_text = tk.StringVar(value='已完成0.0000%')
        progress_label = tk.Label(page2_frame4, textvariable=self.progress_text)
        progress_label.pack(side=tk.RIGHT, fill=tk.X, padx=5)  # 与进度条相邻放置

        # 创建互动次数框架
        page2_frame2 = tk.Frame(page2)
        page2_frame2.pack(pady=10)
        input_label = tk.Label(page2_frame2, text="开始序号:")
        input_label.pack(side=tk.LEFT, padx=5)
        self.interactive_start_input_box = tk.Entry(page2_frame2)
        self.interactive_start_input_box.pack(side=tk.LEFT)

        input_label = tk.Label(page2_frame2, text="互动次数:")
        input_label.pack(side=tk.LEFT, padx=5)
        self.interactive_number_input_box = tk.Entry(page2_frame2)
        self.interactive_number_input_box.pack(side=tk.LEFT)

        auto_like_and_comment_button = tk.Button(page2_frame2, text="开始互动",
                                                 command=lambda: self.interactive.start_interactive_button_click(
                                                     window=page2,
                                                     progress_bar=interactive_progress_bar,
                                                     user_start_index=self.interactive_start_input_box.get(),
                                                     interactive_num=self.interactive_number_input_box.get(),
                                                     progress_text=self.progress_text))
        auto_like_and_comment_button.pack(side=tk.RIGHT, padx=15)

        ##########——————————————自动点赞评论标签页——————————————##########

        ##########——————————————互动用户配置——————————————##########
        page3 = ttk.Frame(notebook)
        notebook.add(page3, text="互动用户配置")

        # 创建数据表格大框架
        page3_frame1 = tk.Frame(page3)
        page3_frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # 创建滚动条
        scrollbar2 = tk.Scrollbar(page3_frame1)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        # 创建Treeview
        user_list_table = ttk.Treeview(page3_frame1, yscrollcommand=scrollbar2.set, selectmode='extended')
        scrollbar2.config(command=user_list_table.yview)
        # 设置列
        user_list_table['columns'] = ("序号", "用户名", "用户ID")
        user_list_table.column("#0", width=0, stretch=tk.NO)
        user_list_table.column("序号", anchor=tk.W, width=100)
        user_list_table.column("用户名", anchor=tk.W, width=200)
        user_list_table.column("用户ID", anchor=tk.W, width=200)
        # 设置列头
        user_list_table.heading("#0", text="", anchor=tk.W)
        user_list_table.heading("序号", text="序号", anchor=tk.W)
        user_list_table.heading("用户名", text="用户名", anchor=tk.W)
        user_list_table.heading("用户ID", text="用户ID", anchor=tk.W)
        # 从数据库中获取数据并插入到Treeview中
        self.data.view_users_data(user_list_table)
        # 绑定鼠标事件
        user_list_table.bind("<<TreeviewSelect>>", self.data.on_row_click)
        user_list_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        # 创建添加用户名、ID、添加数据按钮的大框架
        page3_frame2 = tk.Frame(page3)
        page3_frame2.pack(side=tk.TOP, pady=5)

        # 创建添加用户名框架
        page3_frame2_1 = tk.Frame(page3_frame2)
        page3_frame2_1.pack(side=tk.LEFT, pady=5)
        input_label = tk.Label(page3_frame2_1, text="用户名:")
        input_label.pack(side=tk.LEFT, padx=5)
        self.username_input_box = tk.Entry(page3_frame2_1)
        self.username_input_box.pack(side=tk.RIGHT)

        # 创建添加ID框架
        page3_frame2_2 = tk.Frame(page3_frame2)
        page3_frame2_2.pack(side=tk.LEFT, pady=5)
        id_input_label = tk.Label(page3_frame2_2, text="用户ID:")
        id_input_label.pack(side=tk.LEFT, padx=5)
        self.ID_input_box = tk.Entry(page3_frame2_2)
        self.ID_input_box.pack(side=tk.RIGHT)

        # 添加数据按钮
        page3_frame2_3 = tk.Frame(page3_frame2)
        page3_frame2_3.pack(side=tk.RIGHT, pady=10)
        add_data_button = tk.Button(page3_frame2_3, text="添加用户",
                                    command=lambda: self.data.add_users_data(table=user_list_table,
                                                                             user_name=self.username_input_box.get(),
                                                                             user_id=self.ID_input_box.get(),
                                                                             username_input_box=self.username_input_box,
                                                                             ID_input_box=self.ID_input_box))
        add_data_button.pack(side=tk.RIGHT, padx=10)

        # 删除数据大框架
        page3_frame4 = tk.Frame(page3)
        page3_frame4.pack(side=tk.TOP, pady=5)
        delete_row_data_button = tk.Button(page3_frame4, text="删除选中",
                                           command=lambda: self.data.delete_selected_users_data(table=user_list_table,
                                                                                                database_file='data/interactive_list.db',
                                                                                                table_name="interactive_list",
                                                                                                ))
        delete_row_data_button.pack(side=tk.RIGHT, padx=10)
        delete_all_data_button = tk.Button(page3_frame4, text="删除所有",
                                           command=lambda: self.data.delete_all_data(
                                               database_file='data/interactive_list.db',
                                               table_name="interactive_list",
                                               table_widget=user_list_table))
        delete_all_data_button.pack(side=tk.RIGHT, pady=5)
        ##########————————————————————————————————————————互动用户配置——————————————————————————————————————————##########

        ##########————————————————————————————————————————评论配置——————————————————————————————————————————————##########
        page4 = ttk.Frame(notebook)
        notebook.add(page4, text="评论配置")

        # 创建数据表格大框架
        page4_frame1 = tk.Frame(page4)
        page4_frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # 创建滚动条
        comment_scrollbar = tk.Scrollbar(page4_frame1)
        comment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # 创建Treeview
        comment_table = ttk.Treeview(page4_frame1, yscrollcommand=comment_scrollbar.set)
        comment_scrollbar.config(command=comment_table.yview)
        # 设置列
        comment_table['columns'] = ("序号", "评论内容")
        comment_table.column("#0", width=0, stretch=tk.NO)
        comment_table.column("序号", anchor=tk.W, width=100)
        comment_table.column("评论内容", anchor=tk.W, width=400)
        # 设置列头
        comment_table.heading("#0", text="", anchor=tk.W)
        comment_table.heading("序号", text="序号", anchor=tk.W)
        comment_table.heading("评论内容", text="评论内容", anchor=tk.W)

        # 从数据库中获取数据并插入到Treeview中
        self.data.view_comments_data(table=comment_table)
        comment_table.bind("<<TreeviewSelect>>", self.data.on_row_click)
        comment_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        # 创建添加用户名、ID、添加数据按钮的大框架
        page4_frame2 = tk.Frame(page4)
        page4_frame2.pack(side=tk.TOP, pady=5)
        page4_frame2_2 = tk.Frame(page4_frame2)
        page4_frame2_2.pack(side=tk.LEFT, pady=5)
        comment_input_label = tk.Label(page4_frame2_2, text="评论内容:")
        comment_input_label.pack(side=tk.LEFT, padx=5)
        self.comment_input_box = tk.Entry(page4_frame2_2)
        self.comment_input_box.insert(0, "请输入评论内容")
        self.comment_input_box.pack(side=tk.LEFT)

        # 添加数据按钮
        page4_frame2_3 = tk.Frame(page4_frame2)
        page4_frame2_3.pack(side=tk.RIGHT, pady=10)
        add_comments_data_button = tk.Button(page4_frame2_3, text="添加评论",
                                             command=lambda: self.data.add_comment_data(comment_table=comment_table,
                                                                                        table_name="comments",
                                                                                        comment=self.comment_input_box.get(),
                                                                                        comment_input_box=self.comment_input_box))
        add_comments_data_button.pack(side=tk.RIGHT, padx=10)

        # 删除数据大框架
        page4_frame3 = tk.Frame(page4)
        page4_frame3.pack(side=tk.TOP, pady=5)
        delete_selected_comment_button = tk.Button(page4_frame3, text="删除选中行",
                                                   command=lambda: self.data.delete_selected_comments_data(
                                                       table=comment_table,
                                                       database_file='data/comments_list.db',
                                                       table_name="comments",
                                                   ))
        delete_selected_comment_button.pack(side=tk.RIGHT, padx=10)

        ##########——————————————私信发送——————————————##########
        page7 = ttk.Frame(notebook)
        notebook.add(page7, text="自动私信发送")

        page7_frame0 = tk.Frame(page7)
        page7_frame0.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        self.send_massage_text_box = ScrolledText(page7_frame0, width=900, height=15)
        self.send_massage_text_box.pack()
        self.notice.start_log_update_thread(send_massage_text_box=self.send_massage_text_box, root=page7)

        # 创建进度条大框架
        page7_frame1 = tk.Frame(page7)
        page7_frame1.pack(pady=5)
        # 添加进度条
        progress_label = tk.Label(page7_frame1, text="发送进度: ")
        progress_label.pack(side=tk.LEFT, pady=5)
        massage_progress_bar = ttk.Progressbar(page7_frame1, orient="horizontal", length=450, mode="determinate")
        massage_progress_bar.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        self.massage_progress_text = tk.StringVar(value='已完成0.0000%')
        progress_label = tk.Label(page7_frame1, textvariable=self.massage_progress_text)
        progress_label.pack(side=tk.RIGHT, fill=tk.X, padx=5)  # 与进度条相邻放置

        page7_frame2 = tk.Frame(page7)
        page7_frame2.pack(pady=5)
        # 添加标签和文本框
        start_index_label = tk.Label(page7_frame2, text="开始序号:")
        start_index_label.pack(side=tk.LEFT, padx=5)
        self.start_index_entry = tk.Entry(page7_frame2)
        self.start_index_entry.pack(side=tk.LEFT, padx=5)
        # 创建发送数量大框架
        send_quantity_label = tk.Label(page7_frame2, text="发送数量:")
        send_quantity_label.pack(side=tk.LEFT, padx=5)
        self.send_quantity_entry = tk.Entry(page7_frame2)
        self.send_quantity_entry.pack(side=tk.LEFT, padx=5)
        # 创建消息内容大框架
        page7_frame3 = tk.Frame(page7)
        page7_frame3.pack(pady=5)
        message_label = tk.Label(page7_frame3, text="消息内容:")
        message_label.pack(side=tk.LEFT, padx=5)
        self.message_entry = tk.Entry(page7_frame3, width=52)
        self.message_entry.pack(side=tk.LEFT, padx=5)

        # 添加按钮
        page7_frame4 = tk.Frame(page7)
        page7_frame4.pack(pady=5)
        send_button = tk.Button(page7_frame4, text="开始发送",
                                command=lambda: self.massage.send_massage_button_click(window=page7,
                                                                                       progress_bar=massage_progress_bar,
                                                                                       start_index=self.start_index_entry.get(),
                                                                                       send_quantity=self.send_quantity_entry.get(),
                                                                                       message_data=self.message_entry.get(),
                                                                                       progress_text=self.massage_progress_text))
        send_button.pack()

        ##########——————————————自动私信发送——————————————##########

        ##########——————————————微博爬取——————————————##########
        page8 = ttk.Frame(notebook)
        notebook.add(page8, text="微博爬取")
        page8_frame0 = tk.Frame(page8)
        page8_frame0.pack(side=tk.TOP, fill=tk.X, pady=1)

        canvas = tk.Canvas(page8_frame0)
        canvas.pack(side="left", fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(page8_frame0, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.pack(fill="both", expand=False)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.methods.load_txt_file(scrollable_frame)

        page8_frame1 = tk.Frame(page8)
        page8_frame1.pack(pady=5)
        send_weibo_button = tk.Button(page8_frame1, text="开始发送",
                                command=lambda: self.massage.send_massage_button_click(window=page7,
                                                                                       progress_bar=massage_progress_bar,
                                                                                       start_index=self.start_index_entry.get(),
                                                                                       send_quantity=self.send_quantity_entry.get(),
                                                                                       message_data=self.message_entry.get(),
                                                                                       progress_text=self.massage_progress_text))
        send_weibo_button.pack()

        # 将Notebook组件和按钮放置到主窗口中
        notebook.pack(fill="both", expand=True)
