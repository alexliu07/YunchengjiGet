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
        self.loginBox = None
        self.loginComponent()

        self.root.mainloop()

    def loginComponent(self):
        self.loginBox = ttk.Frame(self.root)
        usernameBox = ttk.Frame(self.loginBox)
        usernameHint = ttk.Label(usernameBox, text='用户名：')
        usernameHint.grid(column=0, row=0, sticky='W',padx=(10,0))
        usernameInput = ttk.Entry(usernameBox,textvariable=self.username)
        usernameInput.grid(column=1, row=0, sticky='W',padx=(0,10))
        usernameBox.grid(column=0, row=0, sticky='E',pady=(10,0))
        passwordBox = ttk.Frame(self.loginBox)
        passwordHint = ttk.Label(passwordBox, text='密码：')
        passwordHint.grid(column=0, row=0, sticky='W',padx=(10,0))
        passwordInput = ttk.Entry(passwordBox,textvariable=self.password,show='*')
        passwordInput.grid(column=1, row=0, sticky='W',padx=(0,10))
        passwordBox.grid(column=0, row=1, sticky='E',pady=(10,0))
        loginButton = ttk.Button(self.loginBox,text='登录')
        loginButton.grid(column=0, row=2, sticky='WE',pady=10,ipadx=30,padx=10)
        self.loginBox.grid(column=0, row=0, sticky='W')

if __name__ == '__main__':
    app = YunchengjiGUI()