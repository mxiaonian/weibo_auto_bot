import tkinter as tk
from gui import Weibo_bot_GUI

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("小念的微博自动机器人")
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")
    # 设置主窗口大小
    root.geometry("650x480")
    # 创建GUI实例
    app = Weibo_bot_GUI(root)
    # 启动Tkinter主循环
    root.mainloop()
