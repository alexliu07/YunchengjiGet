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
        self.login_box = ttk.Frame(self.root)
        self.login_component()

        self.user_box = ttk.Frame(self.root)
        self.student_name = tkinter.StringVar()
        self.student_username = tkinter.StringVar()
        self.student_school = tkinter.StringVar()
        # self.user_component()

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

        self.total_score_result = None
        self.total_gap_result = None
        self.total_result()

        self.root.mainloop()

    def login_component(self):
        """
        登录组件
        :return:None
        """
        username_box = ttk.Frame(self.login_box)
        username_hint = ttk.Label(username_box, text='用户名：')
        username_hint.grid(column=0, row=0, sticky='W')
        username_input = ttk.Entry(username_box,textvariable=self.username,width=20)
        username_input.grid(column=1, row=0, sticky='W')
        username_box.grid(column=0, row=0, sticky='E',pady=(20,0),padx=20)
        password_box = ttk.Frame(self.login_box)
        password_hint = ttk.Label(password_box, text='密码：')
        password_hint.grid(column=0, row=0, sticky='W')
        password_input = ttk.Entry(password_box,textvariable=self.password,show='*',width=20)
        password_input.grid(column=1, row=0, sticky='W')
        password_box.grid(column=0, row=1, sticky='E',pady=(10,0),padx=20)
        login_button = ttk.Button(self.login_box, text='登录')
        login_button.grid(column=0, row=2, sticky='WE',pady=10,padx=20)
        self.login_box.grid(column=0, row=0, sticky='W')

    def user_component(self):
        """
        用户信息显示组件
        :return: None
        """
        student_name_box = ttk.Frame(self.user_box)
        student_name_hint = ttk.Label(student_name_box, text='姓名：')
        student_name_hint.grid(column=0, row=0, sticky='W')
        student_name_display = ttk.Label(student_name_box, textvariable=self.student_name,width=20)
        student_name_display.grid(column=1, row=0, sticky='W')
        student_name_box.grid(column=0, row=0, sticky='E', pady=(20, 0),padx=20)
        username_box = ttk.Frame(self.user_box)
        username_hint = ttk.Label(username_box, text='用户名：')
        username_hint.grid(column=0, row=0, sticky='W')
        username_display = ttk.Label(username_box, textvariable=self.student_username, width=20)
        username_display.grid(column=1, row=0, sticky='W')
        username_box.grid(column=0, row=1, sticky='E', pady=(10, 0),padx=20)
        school_box = ttk.Frame(self.user_box)
        school_hint = ttk.Label(school_box, text='学校：')
        school_hint.grid(column=0, row=0, sticky='W')
        school_display = ttk.Label(school_box, textvariable=self.student_school,width=20)
        school_display.grid(column=1, row=0, sticky='W')
        school_box.grid(column=0, row=2, sticky='E', pady=(10, 0),padx=20)
        logout_button = ttk.Button(self.user_box, text='退出登录')
        logout_button.grid(column=0, row=3, sticky='WE', pady=10,padx=20)
        self.user_box.grid(column=0, row=0, sticky='W')

    def select_component(self):
        """
        考试选择组件
        :return: None
        """
        select_load_box = ttk.Frame(self.root)
        select_box = ttk.Frame(select_load_box)
        select_hint = ttk.Label(select_box, text='请选择考试：')
        select_hint.grid(column=0, row=0, sticky='W')
        select_input = ttk.Combobox(select_box, textvariable=self.select_exam_name,width=50,state='readonly')
        select_input.grid(column=1, row=0, sticky='W')
        select_box.grid(column=0, row=0, sticky='E', pady=(20, 0),padx=20)
        self.custom_box = ttk.Frame(select_load_box)
        custom_hint = ttk.Label(self.custom_box, text='自定义考试ID：')
        custom_hint.grid(column=0, row=0, sticky='W')
        custom_input = ttk.Entry(self.custom_box, textvariable=self.custom_exam_id)
        custom_input.grid(column=1, row=0, sticky='W')
        self.custom_box.grid(column=0, row=1, sticky='W', pady=(10, 0),padx=20)
        self.load_button = ttk.Button(select_load_box, text='加载数据',state='disabled')
        self.load_button.grid(column=0, row=2, sticky='W', pady=10, ipadx=30, padx=20)
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

    def total_result(self):
        """
        全科成绩
        :return: None
        """
        total_box = ttk.Frame(self.result_notebook)
        score_hint = ttk.Label(total_box,text='成绩单')
        score_hint.grid(column=0, row=0, sticky='W', padx=(10, 0),pady=(10,0))
        self.total_score_result = ttk.Treeview(total_box,columns=('score','paperScore','classOrder','schoolOrder','unionOrder'))
        headings1 = ['科目','实际成绩','卷面成绩','班级排名','学校排名','全市排名']
        for i in range(6):
            self.total_score_result.heading(f'#{i}',text=headings1[i])
            self.total_score_result.column(f"#{i}", anchor="center")
        self.total_score_result.grid(column=0, row=1, sticky='W', padx=(10, 0), pady=10)
        gap_hint = ttk.Label(total_box,text='分数差距')
        gap_hint.grid(column=0, row=2, sticky='W', padx=(10, 0),pady=(10,0))
        self.total_gap_result = ttk.Treeview(total_box,columns=('class','school','union'),height=3)
        headings2 = ['数据','班级','学校','全市']
        for i in range(4):
            self.total_gap_result.heading(f'#{i}',text=headings2[i])
            self.total_gap_result.column(f"#{i}", anchor="center")
        self.total_gap_result.grid(column=0, row=3, sticky='W', padx=(10, 0), pady=10)
        self.result_notebook.add(total_box,text='全科')

    def subject_result(self,subject_name):
        """
        单科成绩
        :param subject_name: 科目名称
        :return:Treeview gap,lose,questions
        """
        subject_box = ttk.Frame(self.result_notebook)
        gap_hint = ttk.Label(subject_box, text='分数差距')
        gap_hint.grid(column=0, row=0, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_gap_result = ttk.Treeview(subject_box, columns=('class', 'school', 'union'),height=4)
        headings1 = ['数据', '班级', '学校', '全市']
        for i in range(4):
            subject_gap_result.heading(f'#{i}', text=headings1[i])
            subject_gap_result.column(f"#{i}", anchor="center")
        subject_gap_result.grid(column=0, row=1, sticky='W', padx=(10, 0), pady=10)
        lose_hint = ttk.Label(subject_box, text='难度失分分析')
        lose_hint.grid(column=1, row=0, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_lose_result = ttk.Treeview(subject_box, columns=('easy', 'normal', 'hard'),height=4)
        headings2 = ['数据', '简单题', '中等题', '难题']
        for i in range(4):
            subject_lose_result.heading(f'#{i}', text=headings2[i])
            subject_lose_result.column(f"#{i}", anchor="center")
        subject_lose_result.grid(column=1, row=1, sticky='W', padx=(10, 0), pady=10)
        lose_hint = ttk.Label(subject_box, text='小分情况')
        lose_hint.grid(column=0, row=2, sticky='W', padx=(10, 0), pady=(10, 0))
        subject_question_result = ttk.Treeview(subject_box, columns=('score', 'scoreRate','classScoreRate','schoolScoreRate','unionScoreRate'),height=20)
        headings3 = ['题目', '得分', '我的得分率', '班得分率', '校得分率', '市得分率']
        for i in range(6):
            subject_question_result.heading(f'#{i}',text=headings3[i])
            subject_question_result.column(f"#{i}", anchor="center")
        subject_question_result.grid(column=0, row=3, sticky='W', padx=(10, 0), pady=10,columnspan=2)
        self.result_notebook.add(subject_box,text=subject_name)
        return subject_gap_result,subject_lose_result,subject_question_result

if __name__ == '__main__':
    app = YunchengjiGUI()