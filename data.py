# -*- coding: utf-8 -*-
import random
import sqlite3
from tkinter import messagebox

"""数据库操作类函数"""


class Data:
    def __init__(self):
        self.selected_numbers = []
        self.weibo_url = ''
        self.weibo_login_url = ''
        self.weibo_login_url2 = ''
        self.weibo_login_url3 = ''

    @staticmethod
    def view_users_data(table):
        # 清除treeview中的所有项
        for item in table.get_children():
            table.delete(item)
        # 连接数据库
        conn = sqlite3.connect('data/interactive_list.db')
        cursor = conn.cursor()
        # 获取数据库数据
        cursor.execute("SELECT * FROM interactive_list")
        rows = cursor.fetchall()
        conn.close()
        # 动态生成序号并插入到TreeView中
        for index, row in enumerate(rows, 1):
            table.insert("", 'end', values=(index, row[0], row[1]))

    @staticmethod
    def view_comments_data(table):
        """
        从数据库中获取数据并插入到Treeview中显示
        :param table: Treeview控件
        """
        conn = sqlite3.connect('data/comments_list.db')
        cursor = conn.cursor()
        # 清空Treeview中的数据
        table.delete(*table.get_children())
        # 从数据库中获取数据
        cursor.execute("SELECT 评论内容 FROM comments")
        rows = cursor.fetchall()
        # 插入数据到Treeview中
        for i, row in enumerate(rows, start=1):
            table.insert("", "end", text="", values=(i, row[0]))

        conn.close()

    @staticmethod
    def delete_all_data(database_file, table_name, table_widget):
        conn = sqlite3.connect(database_file)
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name};")
            conn.commit()
            table_widget.delete(*table_widget.get_children())
            messagebox.showinfo("成功", f"表 '{table_name}' 中的所有数据已成功删除。")
        except sqlite3.Error as e:
            messagebox.showerror("错误", f"删除数据时发生数据库错误：{str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"删除数据时发生未知错误：{str(e)}")
        finally:
            conn.close()

    @staticmethod
    def get_random_comments():
        conn = sqlite3.connect('data/comments_list.db')
        cursor = conn.cursor()
        # 从数据库中获取数据
        cursor.execute("SELECT 评论内容 FROM comments")
        comments = cursor.fetchall()
        random_comment = random.choice(comments)
        return random_comment

    def on_row_click(self, event):
        selected_items = event.widget.selection()
        if selected_items:
            self.selected_numbers = [event.widget.item(item)["values"][0] for item in selected_items]  # 列表推导式获取所有序号
        else:
            pass

    def format_username(self, user_name):
        # 删除用户名中的空格（包括中间的空格）和换行符
        return ''.join(user_name.split())

    def add_users_data(self, table, user_name, user_id, username_input_box, ID_input_box):
        conn = sqlite3.connect('data/interactive_list.db')
        cursor = conn.cursor()
        if user_name.strip() == '请输入用户名' and user_id.strip() == '请输入用户ID':
            pass
        elif user_name.strip() == '' or user_id.strip() == '':
            messagebox.showerror("错误", "user_name和user_id不能为空")
        else:
            # 格式化用户名
            formatted_user_name = self.format_username(user_name)
            # 查询数据库以检查是否存在具有相同ID的用户
            cursor.execute('SELECT * FROM interactive_list WHERE 用户ID=?', (user_id,))
            data = cursor.fetchone()
            if data is not None:
                messagebox.showerror("错误", "用户已添加，请勿重复添加")
            else:
                cursor.execute('INSERT INTO interactive_list (用户名, 用户ID) VALUES (?, ?)',
                               (formatted_user_name, user_id))
                conn.commit()
                username_input_box.delete(0, 'end')
                ID_input_box.delete(0, 'end')
                self.refresh_table(table=table, database_file='data/interactive_list.db', table_name='interactive_list')
                table.see(table.get_children()[-1])
                messagebox.showinfo("成功", "数据已成功添加！")
        conn.close()

    def delete_selected_users_data(self, table, database_file, table_name):
        # 获取所有选中项的ID
        selected_items = table.selection()
        delete_numbers = self.selected_numbers
        # 数据库连接
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        for item in selected_items:
            # 获取用户ID
            user_id = table.item(item, 'values')[2]  # 用户ID位于第三列
            # 数据库中删除对应的数据
            cursor.execute(f"DELETE FROM {table_name} WHERE 用户ID=?", (user_id,))
            # 删除TreeView中的行
            table.delete(item)

        # 提交数据库变更
        conn.commit()
        # 断开数据库连接
        conn.close()
        messagebox.showinfo("成功", f"第{delete_numbers}数据已成功删除！")
        # 更新TreeView的行号
        for index, item in enumerate(table.get_children(), start=1):
            table.item(item, values=(index,) + table.item(item, 'values')[1:])

    def delete_selected_comments_data(self, table, database_file, table_name):
        try:
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            delete_numbers = self.selected_numbers
            for delete_number in delete_numbers:
                int(delete_number)
                # 构建delete_data的 SQL 查询语句
                delete_data = f"DELETE FROM {table_name} WHERE rowid = {delete_number};"
                # 执行 SQL 查询
                cursor.execute(delete_data)
                conn.commit()
            # 重新编号行号
            cursor.execute("VACUUM;")
            conn.commit()
            self.refresh_comment_table(table, database_file, table_name)
            messagebox.showinfo("成功", f"第{delete_numbers}数据已成功删除！")
        except sqlite3.Error as e:
            messagebox.showinfo("数据库错误:", str(e))

    def add_comment_data(self, comment_table, table_name, comment, comment_input_box):
        """

        :param comment_table: 在GUI中显示到comment_table中
        :param table_name:数据库的表名
        :param comment: 评论内容
        :param comment_input_box:传入评论输入框
        :return:
        """
        conn = sqlite3.connect('data/comments_list.db')
        cursor = conn.cursor()
        if comment == '请输入评论内容':
            pass
        elif comment == '':
            messagebox.showerror("错误", "不能为空")
        else:
            cursor.execute("INSERT INTO comments (评论内容) VALUES (?)", (comment,))
            conn.commit()
            comment_input_box.delete(0, 'end')
            self.refresh_comment_table(table=comment_table, database_file='data/comments_list.db',
                                       table_name=table_name)
            # 滚动到最后一行
            comment_table.see(comment_table.get_children()[-1])
            messagebox.showinfo("成功", "数据已成功添加！")

        conn.close()

    @staticmethod
    def refresh_table(table, database_file, table_name):
        # 清除treeview中的所有项
        for item in table.get_children():
            table.delete(item)
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        table.delete(*table.get_children())
        for row in rows:
            table.insert('', 'end', values=row)
        conn.close()

    @staticmethod
    def refresh_comment_table(table, database_file, table_name):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        table.delete(*table.get_children())
        # 插入数据到Treeview中
        for i, row in enumerate(rows, start=1):
            table.insert("", "end", text="", values=(i, row[0]))
        conn.close()
