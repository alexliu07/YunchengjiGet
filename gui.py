import os
import threading
import tkinter
import uuid
from tkinter import ttk
from tkinter.ttk import Treeview

import requests.exceptions

from api import YunchengjiAPI

import darkdetect
import sv_ttk


class YunchengjiGUI:
    def __init__(self):
        # 主窗口
        self.root = tkinter.Tk()
        self.root.title('Yunchengji')
        sv_ttk.set_theme(darkdetect.theme())
        self.root.protocol('WM_DELETE_WINDOW', self.on_window_closing)

        # 运行目录
        self.work_dir = os.path.join(os.environ.get('APPDATA', './'), 'yunchengjiget')
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
        self.session_id_path = os.path.join(self.work_dir, 'session_id.txt')

        # 状态常量
        self.login_state = 0

        # 界面组件
        self.login_msg_box = ttk.Frame()
        self.login_button = ttk.Button()
        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.custom_login_msg = tkinter.StringVar()
        self.login_box = ttk.Frame()
        self.login_component()

        self.user_msg_box = ttk.Frame()
        self.user_box = ttk.Frame()
        self.student_name = tkinter.StringVar()
        self.student_username = tkinter.StringVar()
        self.student_school = tkinter.StringVar()
        self.custom_user_msg = tkinter.StringVar()
        self.logout_button = ttk.Button()
        self.user_component()

        self.load_button = ttk.Button()
        self.custom_box = ttk.Frame()
        self.select_input = ttk.Combobox()
        self.custom_exam_id = tkinter.StringVar()
        self.select_exam_name = tkinter.StringVar()
        self.select_component()

        self.result_notebook = ttk.Notebook()
        self.load_hint = ttk.Label()
        self.result_component()

        self.output_xlsx_button = ttk.Button()
        self.output_txt_button = ttk.Button()
        self.action_component()

        self.total_score_result = ttk.Treeview()
        self.total_gap_result = ttk.Treeview()
        self.total_result()

        # API接口
        session_id = str(uuid.uuid4())
        if os.path.exists(self.session_id_path):
            with open(self.session_id_path, "r", encoding='utf-8') as f:
                session_id = f.read()
        self.api = YunchengjiAPI(session_id)

        self.root.mainloop()

    # --------------------------------UI界面部分--------------------------------
    def login_component(self):
        """
        登录组件
        :return:None
        """
        self.login_box = ttk.Frame(self.root)
        username_box = ttk.Frame(self.login_box)
        username_hint = ttk.Label(username_box, text='用户名：')
        username_hint.grid(column=0, row=0, sticky='W')
        username_input = ttk.Entry(username_box, textvariable=self.username, width=20)
        username_input.grid(column=1, row=0, sticky='W')
        username_box.grid(column=0, row=0, sticky='E', pady=(20, 0), padx=20)
        password_box = ttk.Frame(self.login_box)
        password_hint = ttk.Label(password_box, text='密码：')
        password_hint.grid(column=0, row=0, sticky='W')
        password_input = ttk.Entry(password_box, textvariable=self.password, show='*', width=20)
        password_input.grid(column=1, row=0, sticky='W')
        password_box.grid(column=0, row=1, sticky='E', pady=(10, 0), padx=20)
        self.login_button = ttk.Button(self.login_box, text='登录', command=self.start_login_thread)
        self.login_button.grid(column=0, row=2, sticky='WE', pady=(10, 0), padx=20)
        self.login_msg_box = ttk.Frame(self.login_box)
        login_msg_hint = ttk.Label(self.login_msg_box, textvariable=self.custom_login_msg)
        login_msg_hint.grid(column=0, row=0, sticky='W')
        self.login_box.grid(column=0, row=0, sticky='W', pady=(0, 10))

    def show_login_box(self):
        """
        显示登录界面
        :return: None
        """
        self.login_box.grid(column=0, row=0, sticky='W')

    def hide_login_box(self):
        """
        隐藏登录界面
        :return: None
        """
        self.login_box.grid_forget()

    def show_login_msg_box(self):
        """
        显示登录信息
        :return: None
        """
        self.login_msg_box.grid(column=0, row=3, sticky='E', pady=10, padx=20)

    def hide_login_msg_box(self):
        """
        隐藏登录信息
        :return: None
        """
        self.login_msg_box.grid_forget()

    def user_component(self):
        """
        用户信息显示组件
        :return: None
        """
        self.user_box = ttk.Frame(self.root)
        student_name_box = ttk.Frame(self.user_box)
        student_name_hint = ttk.Label(student_name_box, text='姓名：')
        student_name_hint.grid(column=0, row=0, sticky='W')
        student_name_display = ttk.Label(student_name_box, textvariable=self.student_name, width=20)
        student_name_display.grid(column=1, row=0, sticky='W')
        student_name_box.grid(column=0, row=0, sticky='E', pady=(20, 0), padx=20)
        username_box = ttk.Frame(self.user_box)
        username_hint = ttk.Label(username_box, text='用户名：')
        username_hint.grid(column=0, row=0, sticky='W')
        username_display = ttk.Label(username_box, textvariable=self.student_username, width=20)
        username_display.grid(column=1, row=0, sticky='W')
        username_box.grid(column=0, row=1, sticky='E', pady=(10, 0), padx=20)
        school_box = ttk.Frame(self.user_box)
        school_hint = ttk.Label(school_box, text='学校：')
        school_hint.grid(column=0, row=0, sticky='W')
        school_display = ttk.Label(school_box, textvariable=self.student_school, width=20)
        school_display.grid(column=1, row=0, sticky='W')
        school_box.grid(column=0, row=2, sticky='E', pady=(10, 0), padx=20)
        self.logout_button = ttk.Button(self.user_box, text='退出登录', command=self.button_logout)
        self.logout_button.grid(column=0, row=3, sticky='WE', pady=(10, 0), padx=20)
        self.user_msg_box = ttk.Frame(self.user_box)
        user_msg_hint = ttk.Label(self.user_msg_box, textvariable=self.custom_user_msg)
        user_msg_hint.grid(column=0, row=0, sticky='W')
        # self.user_box.grid(column=0, row=0, sticky='W')

    def show_user_box(self):
        """
        显示用户信息
        :return: None
        """
        self.user_box.grid(column=0, row=0, sticky='W', pady=(0, 10))

    def hide_user_box(self):
        """
        隐藏用户信息
        :return: None
        """
        self.user_box.grid_forget()

    def show_user_msg_box(self):
        """
        显示登出信息
        :return: None
        """
        self.user_msg_box.grid(column=0, row=4, sticky='E', pady=10, padx=20)

    def hide_user_msg_box(self):
        """
        隐藏登出信息
        :return: None
        """
        self.user_msg_box.grid_forget()

    def select_component(self):
        """
        考试选择组件
        :return: None
        """
        select_load_box = ttk.Frame(self.root)
        select_box = ttk.Frame(select_load_box)
        select_hint = ttk.Label(select_box, text='请选择考试：')
        select_hint.grid(column=0, row=0, sticky='W')
        self.select_input = ttk.Combobox(select_box, textvariable=self.select_exam_name, width=50, state='readonly')
        self.select_input.bind("<<ComboboxSelected>>", self.on_selected)
        self.select_input.grid(column=1, row=0, sticky='W')
        select_box.grid(column=0, row=0, sticky='E', pady=(20, 0), padx=20)
        self.custom_box = ttk.Frame(select_load_box)
        custom_hint = ttk.Label(self.custom_box, text='自定义考试ID：')
        custom_hint.grid(column=0, row=0, sticky='W')
        custom_input = ttk.Entry(self.custom_box, textvariable=self.custom_exam_id)
        custom_input.grid(column=1, row=0, sticky='W')
        # self.custom_box.grid(column=0, row=1, sticky='W', pady=(10, 0),padx=20)
        self.load_button = ttk.Button(select_load_box, text='加载数据', state='disabled')
        self.load_button.grid(column=0, row=2, sticky='W', pady=10, ipadx=30, padx=20)
        select_load_box.grid(column=1, row=0, sticky='W')

    def show_custom_box(self):
        """
        显示自定义考试id输入框
        :return: None
        """
        self.custom_box.grid(column=0, row=1, sticky='W', pady=(10, 0), padx=20)

    def hide_custom_box(self):
        """
        隐藏自定义考试id输入框
        :return: None
        """
        self.custom_box.grid_forget()

    def result_component(self):
        """
        结果展示组件
        :return: None
        """
        result_box = ttk.Frame(self.root)
        self.load_hint = ttk.Label(result_box, text='请先登录、选择考试并加载数据')
        self.load_hint.grid(column=0, row=0, sticky='WE', padx=(10, 0), pady=10)
        self.result_notebook = ttk.Notebook(result_box)
        # self.result_notebook.grid(column=0, row=1, sticky='WE', padx=(10, 0),pady=10)
        result_box.grid(column=0, row=1, sticky='WE', columnspan=2)

    def action_component(self):
        """
        操作组件
        :return: None
        """
        action_box = ttk.Frame(self.root)
        self.output_txt_button = ttk.Button(action_box, text='导出为文本文件', state='disabled')
        self.output_txt_button.grid(column=0, row=0, sticky='E', padx=(0, 10), pady=10)
        self.output_xlsx_button = ttk.Button(action_box, text='导出为表格文件', state='disabled')
        self.output_xlsx_button.grid(column=1, row=0, sticky='E', padx=(0, 10), pady=10)
        action_box.grid(column=1, row=2, sticky='E', pady=(10, 0))

    def total_result(self):
        """
        全科成绩
        :return: None
        """
        total_box = ttk.Frame(self.result_notebook)
        score_hint = ttk.Label(total_box, text='成绩单')
        score_hint.grid(column=0, row=0, sticky='W', padx=(10, 0), pady=(10, 0))
        self.total_score_result = ttk.Treeview(total_box, columns=('score', 'paperScore', 'classOrder', 'schoolOrder',
                                                                   'unionOrder'))
        headings1 = ['科目', '实际成绩', '卷面成绩', '班级排名', '学校排名', '全市排名']
        for i in range(6):
            self.total_score_result.heading(f'#{i}', text=headings1[i])
            self.total_score_result.column(f"#{i}", anchor="center")
        self.total_score_result.grid(column=0, row=1, sticky='W', padx=(10, 0), pady=10)
        gap_hint = ttk.Label(total_box, text='分数差距')
        gap_hint.grid(column=0, row=2, sticky='W', padx=(10, 0), pady=(10, 0))
        self.total_gap_result = ttk.Treeview(total_box, columns=('class', 'school', 'union'), height=3)
        headings2 = ['数据', '班级', '学校', '全市']
        for i in range(4):
            self.total_gap_result.heading(f'#{i}', text=headings2[i])
            self.total_gap_result.column(f"#{i}", anchor="center")
        self.total_gap_result.grid(column=0, row=3, sticky='W', padx=(10, 0), pady=10)
        self.result_notebook.add(total_box, text='全科')

    def subject_result(self, subject_name: str) -> tuple[Treeview, Treeview, Treeview]:
        """
        单科成绩
        :param subject_name: 科目名称
        :return:Treeview gap,lose,questions
        """
        subject_box = ttk.Frame(self.result_notebook)
        score_hint = ttk.Label(subject_box, text='成绩')
        score_hint.grid(column=0, row=0, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_score_result = ttk.Treeview(subject_box,
                                            columns=('score', 'paperScore', 'classOrder', 'schoolOrder', 'unionOrder'),
                                            height=1)
        headings1 = ['科目', '实际成绩', '卷面成绩', '班级排名', '学校排名', '全市排名']
        for i in range(6):
            subject_score_result.heading(f'#{i}', text=headings1[i])
            subject_score_result.column(f"#{i}", anchor="center")
        subject_score_result.grid(column=0, row=1, sticky='W', padx=(10, 0), pady=10, columnspan=2)
        gap_hint = ttk.Label(subject_box, text='分数差距')
        gap_hint.grid(column=0, row=2, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_gap_result = ttk.Treeview(subject_box, columns=('class', 'school', 'union'), height=4)
        headings2 = ['数据', '班级', '学校', '全市']
        for i in range(4):
            subject_gap_result.heading(f'#{i}', text=headings2[i])
            subject_gap_result.column(f"#{i}", anchor="center")
        subject_gap_result.grid(column=0, row=3, sticky='W', padx=(10, 0), pady=10)
        lose_hint = ttk.Label(subject_box, text='难度失分分析')
        lose_hint.grid(column=1, row=2, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_lose_result = ttk.Treeview(subject_box, columns=('easy', 'normal', 'hard'), height=4)
        headings3 = ['数据', '简单题', '中等题', '难题']
        for i in range(4):
            subject_lose_result.heading(f'#{i}', text=headings3[i])
            subject_lose_result.column(f"#{i}", anchor="center")
        subject_lose_result.grid(column=1, row=3, sticky='W', padx=(10, 0), pady=10)
        question_hint = ttk.Label(subject_box, text='小分情况')
        question_hint.grid(column=0, row=4, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_question_result = ttk.Treeview(subject_box,
                                               columns=('score', 'scoreRate', 'classScoreRate', 'schoolScoreRate',
                                                        'unionScoreRate'), height=20)
        headings4 = ['题目', '得分', '我的得分率', '班得分率', '校得分率', '市得分率']
        for i in range(6):
            subject_question_result.heading(f'#{i}', text=headings4[i])
            subject_question_result.column(f"#{i}", anchor="center")
        subject_question_result.grid(column=0, row=5, sticky='W', padx=(10, 0), pady=10, columnspan=2)
        self.result_notebook.add(subject_box, text=subject_name)
        return subject_gap_result, subject_lose_result, subject_question_result

    # --------------------------------程序逻辑部分--------------------------------
    def login(self):
        """
        执行登录操作
        :return: None
        """
        try:
            login_result = self.api.login(self.username.get(), self.password.get())
        except requests.exceptions.RequestException:
            self.custom_login_msg.set('网络错误')
            return
        if login_result == -1:
            self.custom_login_msg.set('用户名或密码错误')
            return
        try:
            user_info = self.api.get_user_info()
        except requests.exceptions.RequestException:
            self.custom_login_msg.set('网络错误')
            return
        self.login_state = 1
        self.student_name.set(user_info['childname'])
        self.student_username.set(user_info['studentusername'])
        self.student_school.set(user_info['schoolname'])
        self.hide_login_box()
        self.hide_login_msg_box()
        self.show_user_box()
        self.login_button.configure(state='normal')
        # 填充考试列表
        self.start_fill_thread()

    def start_login_thread(self):
        """
        启动登录线程
        :return: None
        """
        self.login_button.configure(state='disabled')
        self.custom_login_msg.set('登录中...')
        self.show_login_msg_box()
        login_thread = threading.Thread(target=self.login)
        login_thread.start()

    def logout(self, mode: str):
        """
        程序内登出
        :return: None
        """
        self.login_state = 0
        try:
            new_session_id = self.api.logout()
        except requests.exceptions.RequestException:
            if mode == 'button':
                self.custom_user_msg.set('网络错误')
            elif mode == 'window':
                self.root.quit()
            return
        with open(self.session_id_path, 'w+', encoding='utf-8') as f:
            f.write(new_session_id)
        # 清除内容
        if mode == 'button':
            self.select_input['values'] = []
            self.hide_user_msg_box()
            self.hide_user_box()
            self.show_login_box()
            self.logout_button.configure(state='normal')
        elif mode == 'window':
            self.root.quit()

    def start_logout_thread(self, mode: str):
        """
        启动登出线程
        :return: None
        """
        self.logout_button.configure(state='disabled')
        self.custom_user_msg.set('退出登录中...')
        self.show_user_msg_box()
        logout_thread = threading.Thread(target=self.logout, args=(mode,))
        logout_thread.start()

    def button_logout(self):
        """
        使用按钮登出
        :return: None
        """
        self.start_logout_thread('button')

    def on_window_closing(self):
        """
        退出程序时登出
        :return: None
        """
        if self.login_state == 1:
            self.start_logout_thread('window')
        else:
            self.root.quit()

    def fill_exam_list(self):
        """
        填充考试列表
        :return: None
        """
        try:
            result = self.api.get_exam_list()
        except requests.exceptions.RequestException:
            self.custom_user_msg.set('网络错误')
            return
        exam_list = {}
        names = []
        for i in result:
            exam_list[i['name']] = i['id']
            names.append(i['name'])
        names.append('自定义考试')
        self.select_input['values'] = names
        self.hide_user_msg_box()

    def start_fill_thread(self):
        """
        开启填充考试列表线程
        :return: None
        """
        self.custom_user_msg.set('获取考试列表中...')
        self.show_user_msg_box()
        fill_thread = threading.Thread(target=self.fill_exam_list)
        fill_thread.start()

    def on_selected(self, event:tkinter.Event):
        """
        选中考试时触发
        :param event: tkinter.Event 必须接收该参数，否则报错
        :return: None
        """
        result = self.select_input.get()
        if result == '':
            return
        if result == '自定义考试':
            self.show_custom_box()
        else:
            self.hide_custom_box()
        self.load_button.config(state='normal')


if __name__ == '__main__':
    app = YunchengjiGUI()
