import os
import threading
import tkinter
import uuid
from tkinter import ttk,filedialog

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

        # 相关路径
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
        self.select_component()

        self.custom_load_msg = tkinter.StringVar()
        self.custom_load_msg.set('请先登录、选择考试并加载数据')
        self.result_notebook = ttk.Notebook()
        self.load_hint = ttk.Label()
        self.result_component()

        self.output_xlsx_button = ttk.Button()
        self.output_txt_button = ttk.Button()
        self.custom_save_msg = tkinter.StringVar()
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

        # 考试信息
        self.exam_list = {}
        self.target_exam_id = ''
        self.exam_result_total = {}
        self.subject_list = []
        self.exam_result_subject = {}
        self.exam_result_subject_questions = {}

        # 加载数据
        self.total_thread = threading.Thread()
        self.subject_thread = threading.Thread()
        self.lock = threading.Lock()

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
        self.select_input = ttk.Combobox(select_box, width=50, state='readonly')
        self.select_input.bind("<<ComboboxSelected>>", self.on_selected)
        self.select_input.grid(column=1, row=0, sticky='W')
        select_box.grid(column=0, row=0, sticky='E', pady=(20, 0), padx=20)
        self.custom_box = ttk.Frame(select_load_box)
        custom_hint = ttk.Label(self.custom_box, text='自定义考试ID：')
        custom_hint.grid(column=0, row=0, sticky='W')
        custom_input = ttk.Entry(self.custom_box, textvariable=self.custom_exam_id)
        custom_input.grid(column=1, row=0, sticky='W')
        # self.custom_box.grid(column=0, row=1, sticky='W', pady=(10, 0),padx=20)
        self.load_button = ttk.Button(select_load_box, text='加载数据', state='disabled',command=self.load_result)
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
        self.load_hint = ttk.Label(result_box, textvariable=self.custom_load_msg)
        self.load_hint.grid(column=0, row=0, sticky='WE', padx=(10, 0), pady=10)
        self.result_notebook = ttk.Notebook(result_box)
        # self.result_notebook.grid(column=0, row=1, sticky='WE', padx=(10, 0),pady=10)
        result_box.grid(column=0, row=1, sticky='WE', columnspan=2)

    def show_result_notebook(self):
        """
        显示结果
        :return: None
        """
        self.result_notebook.grid(column=0, row=1, sticky='WE', padx=(10, 0), pady=10)

    def hide_result_notebook(self):
        """
        隐藏结果
        :return: None
        """
        self.result_notebook.grid_forget()

    def action_component(self):
        """
        操作组件
        :return: None
        """
        action_box = ttk.Frame(self.root)
        hint_text = ttk.Label(action_box,textvariable=self.custom_save_msg)
        hint_text.grid(column=0, row=0, sticky='E', padx=(0, 10), pady=10)
        self.output_txt_button = ttk.Button(action_box, text='导出为文本文件', state='disabled',command=self.save_to_txt)
        self.output_txt_button.grid(column=1, row=0, sticky='E', padx=(0, 10), pady=10)
        self.output_xlsx_button = ttk.Button(action_box, text='导出为表格文件', state='disabled')
        self.output_xlsx_button.grid(column=2, row=0, sticky='E', padx=(0, 10), pady=10)
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
        scroll_bar = ttk.Scrollbar(total_box,orient='vertical',command=self.total_score_result.yview)
        self.total_score_result.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(column=1, row=1, sticky='NS')
        gap_hint = ttk.Label(total_box, text='分数差距')
        gap_hint.grid(column=0, row=2, sticky='W', padx=(10, 0), pady=(10, 0))
        self.total_gap_result = ttk.Treeview(total_box, columns=('class', 'school', 'union'), height=3)
        headings2 = ['数据', '班级', '学校', '全市']
        for i in range(4):
            self.total_gap_result.heading(f'#{i}', text=headings2[i])
            self.total_gap_result.column(f"#{i}", anchor="center")
        self.total_gap_result.grid(column=0, row=3, sticky='W', padx=(10, 0), pady=10)
        self.result_notebook.add(total_box, text='全科')

    def subject_result(self, subject_name: str) -> tuple[ttk.Treeview,ttk.Treeview, ttk.Treeview, ttk.Treeview]:
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
        scroll_bar = ttk.Scrollbar(subject_box,orient='vertical',command=subject_question_result.yview)
        subject_question_result.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.grid(column=1, row=5, sticky='NS')
        self.result_notebook.add(subject_box, text=subject_name)
        return subject_score_result, subject_gap_result, subject_lose_result, subject_question_result

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
            self.output_txt_button.configure(state='disabled')
            self.output_xlsx_button.configure(state='disabled')
            self.load_button.configure(state='disabled')
            self.select_input.set('')
            self.hide_custom_box()
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
        self.clear_data()
        self.custom_load_msg.set('请先登录、选择考试并加载数据')

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
        self.exam_list = {}
        names = []
        for i in result:
            self.exam_list[i['name']] = i['id']
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

    def result_total(self):
        """
        获取全科信息并填充
        :return: None
        """
        self.exam_result_total = self.api.get_exam_detail_total(self.target_exam_id)
        for i in self.exam_result_total['stuOrder']['subjects']:
            self.total_score_result.insert("",index='end',text=i['name'],values=('{}/{}'.format(i['score'],i['fullScore']),'{}/{}'.format(i['paperScore'],i['fullScore']),i['classOrder'],i['schoolOrder'],i['unionOrder']))
        names = ['考生数','最高分','平均分']
        datas = ['Num','Top','Avg']
        score_gap = self.exam_result_total['stuOrder']['scoreGap']
        for i in range(3):
            self.total_gap_result.insert("",index='end',text=names[i],values=(score_gap['class{}'.format(datas[i])],score_gap['school{}'.format(datas[i])],score_gap['union{}'.format(datas[i])]))

    def result_each_subject(self,subject_id:int,score_result:ttk.Treeview, gap_result:ttk.Treeview, lose_result:ttk.Treeview, question_result:ttk.Treeview):
        """
        获取并填充单科信息
        :param question_result: treeview
        :param lose_result: treeview
        :param gap_result: treeview
        :param score_result: treeview
        :param subject_id: 科目id
        :return:None
        """
        result1 = self.api.get_exam_detail_subject(self.target_exam_id, subject_id)
        result2 = self.api.get_exam_detail_subject_questions(self.target_exam_id, subject_id)
        self.lock.acquire()
        self.exam_result_subject[subject_id] = result1
        self.exam_result_subject_questions[subject_id] = result2
        self.lock.release()
        for i in self.exam_result_total['stuOrder']['subjects']:
            if i['id'] == subject_id:
                score_result.insert("",index='end',text=i['name'],values=('{}/{}'.format(i['score'],i['fullScore']),'{}/{}'.format(i['paperScore'],i['fullScore']),i['classOrder'],i['schoolOrder'],i['unionOrder']))
                break
        names1 = ['考生数', '最高分', '平均分']
        datas1 = ['Num', 'Top', 'Avg']
        score_gap = result1['stuOrder']['scoreGap']
        for i in range(3):
            gap_result.insert("", index='end', text=names1[i], values=(score_gap['class{}'.format(datas1[i])],
                                                                                 score_gap['school{}'.format(datas1[i])],
                                                                                 score_gap['union{}'.format(datas1[i])]))
        names2 = ['题量','分值','丢分','得分率']
        datas2=['ScoreCount','TotalScore','Score','TotalRateScore']
        for i in range(4):
            lose_result.insert("",index='end',text=names2[i],values=(result1['lose{}1'.format(datas2[i])],result1['lose{}2'.format(datas2[i])],result1['lose{}3'.format(datas2[i])]))
        for i in range(len(result1['questRates'])):
            question_result.insert("",index='end',text=result1['questRates'][i]['title'],values=('{}/{}'.format(result2[i]['score'],result2[i]['totalScore']),result1['questRates'][i]['scoreRate'],result1['questRates'][i]['classScoreRate'],result1['questRates'][i]['schoolScoreRate'],result1['questRates'][i]['unionScoreRate']))

    def result_subjects(self):
        """
        获取所有单科信息并填充
        :return: None
        """
        # 获取科目列表
        self.subject_list = self.api.get_subject_list(self.target_exam_id)
        threads = []
        # 获取成绩
        for i in self.subject_list:
            score_result, gap_result, lose_result, question_result = self.subject_result(i['name'])
            thread = threading.Thread(target=self.result_each_subject,args=(i['id'],score_result, gap_result, lose_result, question_result))
            thread.start()
            threads.append(thread)
        for i in threads:
            i.join()

    def load_result(self):
        """
        加载数据
        :return: None
        """
        self.load_button.configure(state='disabled')
        self.output_txt_button.configure(state='disabled')
        self.output_xlsx_button.configure(state='disabled')
        # 清空数据
        self.clear_data()
        select = self.select_input.get()
        if select == '自定义考试':
            self.target_exam_id = self.custom_exam_id.get()
        else:
            self.target_exam_id = self.exam_list[select]
        self.custom_load_msg.set('加载数据中...')
        self.total_thread = threading.Thread(target=self.result_total)
        self.total_thread.start()
        self.subject_thread = threading.Thread(target=self.result_subjects)
        self.subject_thread.start()
        wait_thread = threading.Thread(target=self.wait_for_loading)
        wait_thread.start()

    def clear_data(self):
        """
        清空数据
        :return: None
        """
        self.hide_result_notebook()
        self.custom_save_msg.set('')
        self.total_score_result.delete(*self.total_score_result.get_children())
        self.total_gap_result.delete(*self.total_gap_result.get_children())
        for i in self.result_notebook.winfo_children():
            i.destroy()
        self.total_result()


    def wait_for_loading(self):
        """
        等待所有数据加载完成
        :return: None
        """
        self.total_thread.join()
        self.subject_thread.join()
        self.custom_load_msg.set(self.exam_result_total['examName'])
        self.show_result_notebook()
        self.load_button.configure(state='normal')
        self.output_xlsx_button.configure(state='normal')
        self.output_txt_button.configure(state='normal')

    def output_txt(self,path:str):
        """
        将结果输出到txt文件
        :param path 路径
        :return: None
        """
        text1 = '{}  实际成绩：{:<7}/{:<7} 卷面成绩：{:<7}/{:<7} 班级排名：{:<3} 学校排名：{:<5} 全市排名：{:<6}'
        text2 = '考生数  班级：{:<7} 学校：{:<7} 全市：{:<7}\n最高分  班级：{:<7} 学校：{:<7} 全市：{:<7}\n平均分  班级：{:<7} 学校：{:<7} 全市：{:<7}'
        text3 = '题量  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n分值  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n丢分  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n得分  简单题：{:<7} 中等题：{:<7} 难题：{:<7}'
        text4 = '{:<8} 得分：{:<5}/{:<5} 我的得分率：{:<7} 班得分率：{:<7} 校得分率：{:<7} 市得分率：{:<7}'
        output = [self.exam_result_total['examName'], '全科', '成绩单']
        for subject in self.exam_result_total['stuOrder']['subjects']:
            output.append(text1.format(subject['name'], subject['score'], subject['fullScore'], subject['paperScore'],
                                       subject['fullScore'], subject['classOrder'], subject['schoolOrder'],
                                       subject['unionOrder']))
        output.append('分数差距')
        score_gap = self.exam_result_total['stuOrder']['scoreGap']
        output.append(
            text2.format(score_gap['classNum'], score_gap['schoolNum'], score_gap['unionNum'], score_gap['classTop'],
                         score_gap['schoolTop'], score_gap['unionTop'], score_gap['classAvg'], score_gap['schoolAvg'],
                         score_gap['unionAvg']))
        output.append('')
        for subject in self.subject_list:
            output.append(subject['name'])
            for i in self.exam_result_total['stuOrder']['subjects']:
                if i['id'] == subject['id']:
                    output.append(text1.format(i['name'], i['score'], i['fullScore'], i['paperScore'],
                                       i['fullScore'], i['classOrder'], i['schoolOrder'],
                                       i['unionOrder']))
                    break
            output.append('分数差距')
            score_gap = self.exam_result_subject[subject['id']]['stuOrder']['scoreGap']
            output.append(
                text2.format(score_gap['classNum'], score_gap['schoolNum'], score_gap['unionNum'], score_gap['classTop'],
                             score_gap['schoolTop'], score_gap['unionTop'], score_gap['classAvg'], score_gap['schoolAvg'],
                             score_gap['unionAvg']))
            output.append('难度失分分析')
            output.append(text3.format(self.exam_result_subject[subject['id']]['loseScoreCount1'], self.exam_result_subject[subject['id']]['loseScoreCount2'],
                                       self.exam_result_subject[subject['id']]['loseScoreCount3'], self.exam_result_subject[subject['id']]['loseTotalScore1'],
                                       self.exam_result_subject[subject['id']]['loseTotalScore2'], self.exam_result_subject[subject['id']]['loseTotalScore3'],
                                       self.exam_result_subject[subject['id']]['loseScore1'], self.exam_result_subject[subject['id']]['loseScore2'],
                                       self.exam_result_subject[subject['id']]['loseScore3'], self.exam_result_subject[subject['id']]['loseTotalRateScore1'],
                                       self.exam_result_subject[subject['id']]['loseTotalRateScore2'], self.exam_result_subject[subject['id']]['loseTotalRateScore3']))
            output.append('小分情况')
            for j in range(len(self.exam_result_subject[subject['id']]['questRates'])):
                output.append(text4.format(self.exam_result_subject[subject['id']]['questRates'][j]['title'], self.exam_result_subject_questions[subject['id']][j]['score'],
                                           self.exam_result_subject_questions[subject['id']][j]['totalScore'], self.exam_result_subject[subject['id']]['questRates'][j]['scoreRate'],
                                           self.exam_result_subject[subject['id']]['questRates'][j]['classScoreRate'],
                                           self.exam_result_subject[subject['id']]['questRates'][j]['schoolScoreRate'],
                                           self.exam_result_subject[subject['id']]['questRates'][j]['unionScoreRate']))
            output.append('')
        with open(path,'w+',encoding='utf-8') as f:
            f.write('\n'.join(output))
        self.custom_save_msg.set('数据已保存')

    def save_to_txt(self):
        """
        将结果保存到文本文件
        :return: None
        """
        path = filedialog.asksaveasfilename(title='导出为文本文件',filetypes=(('文本文件','.txt'),),initialfile='{}-{}'.format(self.student_name.get(),self.exam_result_total['examName']),defaultextension='.txt')
        self.custom_save_msg.set('保存中...')
        save_thread = threading.Thread(target=self.output_txt, args=(path,))
        save_thread.start()

if __name__ == '__main__':
    app = YunchengjiGUI()
