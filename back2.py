import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.messagebox as messagebox
from tkinter import *
import xlrd
import xlwt
import numpy as np
def back2():
    data = xlrd.open_workbook(r'my.xls')
    sh1= data.sheet_by_name('温度')
    sh= data.sheet_by_name('挠度')
    sh2= data.sheet_by_name('应变')
    root2 = Tk()
    root2.title("数据可视化")
    root2.geometry("500x500")
    f = Figure(figsize=(2.52, 2.56), dpi=100)#figsize定义图像大小，dpi定义像素
    f_plot = f.add_subplot(111)#定义画布中的位置
    canvs = FigureCanvasTkAgg(f, root2)#f是定义的图像，root是tkinter中画布的定义位置
    canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    Label(root2,text="*位移点A-R,温度点A-M,应变点1-44*",font=50).pack()
    Label(root2,text="选择温度",font=20).pack()
    user_text=Entry(root2)
    user_text.pack()
    def draw_T():  
        f_plot.clear()
        t =ord(user_text.get()) #用字母表示时
        if t>77:
            str1 = messagebox.showinfo(title='提示',message = '输入范围错误，请重新输入')
            if str1 == 'ok':
                return
        test_TEM = t-65
        if test_TEM<13:
            col_test_TEM = sh1.col_values(test_TEM)
            x=np.arange(0,1078,1)
            y=np.array(col_test_TEM[1:])                               
            f_plot.set(title='temprature_self',xlabel='time/10min',ylabel='temprature')
            f_plot.plot(x,y)                                                                
            canvs.draw() 
    Button(root2, text='选择测试点', command=draw_T).pack()
    Label(root2,text="选择位移",font=20).pack()
    user_text1=Entry(root2)
    user_text1.pack()
    def draw_D():
        f_plot.clear()
        d =ord(user_text1.get())#用字母表示时
        if d>82:
            str1 = messagebox.showinfo(title='提示',message = '输入范围错误，请重新输入')
            if str1 == 'ok':
                return
        test_VD = d-65
        if test_VD<18:
            col_test_VD = sh.col_values(test_VD)
            x=np.arange(0,1078,1)
            y=np.array(col_test_VD[1:])
            f_plot.set(title='ver_d_self',xlabel='time/10min',ylabel='ver_d')
            f_plot.plot(x,y)
            canvs.draw()
    Button(root2,text='选择测试点',command=draw_D).pack()
    Label(root2,text="选择应变",font=20).pack()
    user_text2=Entry(root2)
    user_text2.pack()

    root2.mainloop()