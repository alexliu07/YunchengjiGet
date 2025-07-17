import tkinter
from tkinter import ttk

import darkdetect
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

        self.load_button = None
        self.custom_box = None
        self.custom_exam_id = tkinter.StringVar()
        self.select_exam_name = tkinter.StringVar()
        self.select_component()

        self.result_notebook = None
        self.load_hint = None
        self.result_component()

        self.output_xlsx_button = None
        self.output_txt_button = None
        self.action_component()

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
        select_load_box = ttk.Frame(self.root)
        select_box = ttk.Frame(select_load_box)
        select_hint = ttk.Label(select_box, text='请选择考试：')
        select_hint.grid(column=0, row=0, sticky='W', padx=(10, 0))
        select_input = ttk.Combobox(select_box, textvariable=self.select_exam_name,width=50,state='readonly')
        select_input['value'] = '请先登录'
        select_input.grid(column=1, row=0, sticky='W', padx=(0, 10))
        select_box.grid(column=0, row=0, sticky='E', pady=(10, 0))
        self.custom_box = ttk.Frame(select_load_box)
        custom_hint = ttk.Label(self.custom_box, text='自定义考试ID：')
        custom_hint.grid(column=0, row=0, sticky='W', padx=(10, 0))
        custom_input = ttk.Entry(self.custom_box, textvariable=self.custom_exam_id)
        custom_input.grid(column=1, row=0, sticky='W', padx=(0, 10))
        self.custom_box.grid(column=0, row=1, sticky='W', pady=(10, 0))
        self.load_button = ttk.Button(select_load_box, text='加载数据',state='disabled')
        self.load_button.grid(column=0, row=2, sticky='W', pady=10, ipadx=30, padx=10)
        select_load_box.grid(column=1, row=0, sticky='W')

    def result_component(self):
        """
        结果展示组件
        :return: None
        """
        result_box = ttk.Frame(self.root)
        self.load_hint = ttk.Label(result_box,text='请先选择考试并加载数据')
        self.load_hint.grid(column=0, row=0, sticky='WE', padx=(10, 0),pady=10)
        self.result_notebook = ttk.Notebook(result_box)
        # self.result_notebook.grid(column=0, row=1, sticky='WE', padx=(10, 0),pady=10)
        result_box.grid(column=0, row=1, sticky='WE',columnspan=2)

    def action_component(self):
        """
        操作组件
        :return: None
        """
        action_box = ttk.Frame(self.root)
        self.output_txt_button = ttk.Button(action_box,text='导出为文本文件',state='disabled')
        self.output_txt_button.grid(column=0, row=0, sticky='E', padx=(0, 10),pady=10)
        self.output_xlsx_button = ttk.Button(action_box,text='导出为表格文件',state='disabled')
        self.output_xlsx_button.grid(column=1, row=0, sticky='E', padx=(0, 10),pady=10)
        action_box.grid(column=1, row=2, sticky='E', pady=(10, 0))


if __name__ == '__main__':
    app = YunchengjiGUI()