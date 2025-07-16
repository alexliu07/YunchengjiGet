import sys
import tkinter
from tkinter import ttk

import darkdetect
import pywinstyles
import sv_ttk


class YunchengjiGUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Yunchengji')
        sv_ttk.set_theme(darkdetect.theme())

        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.login_box = None
        self.login_component()

        self.select_load_box = None
        self.custom_exam_id = tkinter.StringVar()
        self.select_exam_name = tkinter.StringVar()
        self.select_component()

        self.root.mainloop()

    def login_component(self):
        """
        登录组件
        :return:None
        """
        self.login_box = ttk.Frame(self.root)
        username_box = ttk.Frame(self.login_box)
        username_hint = ttk.Label(username_box, text='用户名：')
        username_hint.grid(column=0, row=0, sticky='W',padx=(10,0))
        username_input = ttk.Entry(username_box,textvariable=self.username)
        username_input.grid(column=1, row=0, sticky='W',padx=(0,10))
        username_box.grid(column=0, row=0, sticky='E',pady=(10,0))
        password_box = ttk.Frame(self.login_box)
        password_hint = ttk.Label(password_box, text='密码：')
        password_hint.grid(column=0, row=0, sticky='W',padx=(10,0))
        password_input = ttk.Entry(password_box,textvariable=self.password,show='*')
        password_input.grid(column=1, row=0, sticky='W',padx=(0,10))
        password_box.grid(column=0, row=1, sticky='E',pady=(10,0))
        login_button = ttk.Button(self.login_box, text='登录')
        login_button.grid(column=0, row=2, sticky='WE',pady=10,padx=10)
        self.login_box.grid(column=0, row=0, sticky='W')

    def select_component(self):
        """
        考试选择组件
        :return: None
        """
        self.select_load_box = ttk.Frame(self.root)
        select_box = ttk.Frame(self.select_load_box)
        select_hint = ttk.Label(select_box, text='请选择考试：')
        select_hint.grid(column=0, row=0, sticky='W', padx=(10, 0))
        select_input = ttk.Combobox(select_box, textvariable=self.select_exam_name,width=50,state='readonly')
        select_input['value'] = '请先登录'
        select_input.grid(column=1, row=0, sticky='W', padx=(0, 10))
        select_box.grid(column=0, row=0, sticky='E', pady=(10, 0))
        custom_box = ttk.Frame(self.select_load_box)
        custom_hint = ttk.Label(custom_box, text='自定义考试ID：')
        custom_hint.grid(column=0, row=0, sticky='W', padx=(10, 0))
        custom_input = ttk.Entry(custom_box, textvariable=self.custom_exam_id)
        custom_input.grid(column=1, row=0, sticky='W', padx=(0, 10))
        custom_box.grid(column=0, row=1, sticky='W', pady=(10, 0))
        load_button = ttk.Button(self.select_load_box, text='加载数据',state='disabled')
        load_button.grid(column=0, row=2, sticky='W', pady=10, ipadx=30, padx=10)
        self.select_load_box.grid(column=1, row=0, sticky='W')


if __name__ == '__main__':
    app = YunchengjiGUI()