import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import StringVar
import back
root = tk.Tk()
root.title('登陆')
tk.Label(root, text="账号：",font=20).grid(row=0, column=0)
tk.Label(root, font=20,text="密码：").grid(row=1, column=0)
e1=tk.Entry(root, textvariable=StringVar())
e1.grid(row=0, column=1)
e2=tk.Entry(root, show="●",textvariable=StringVar())
e2.grid(row=1, column=1)
def show():
    if e1.get() == '1'and e2.get() == '1':
        str1 = tk.messagebox.showinfo(title='提示',message = '恭喜密码正确')
        if str1 == 'ok':
            root.destroy()
            back.back()
    else :
        string_a = '密码或账号错误 ，请重新输入！'
        messagebox.showinfo(title='提示', message = string_a)
tk.Button(root, text="登 陆", font=12,width=10,command=show).grid(row=2, column=0)
tk.Button(root, text="注 册", font=12,width=10,).grid(row=2, column=1)
tk.Button(root, text="退 出", font=12,width=10, command=root.destroy).grid(row=2, column=2)
root.mainloop()