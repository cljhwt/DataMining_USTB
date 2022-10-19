import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import xlrd
import xlwt
import numpy as np
data = xlrd.open_workbook(r'my.xls')
sh1= data.sheet_by_name('温度')
sh= data.sheet_by_name('挠度')
sh2= data.sheet_by_name('应变')
root = Tk()
root.title("数据可视化")
root.geometry("500x500")
f = Figure(figsize=(2.52, 2.56), dpi=100)#figsize定义图像大小，dpi定义像素
f_plot = f.add_subplot(111)#定义画布中的位置
canvs = FigureCanvasTkAgg(f, root)#f是定义的图像，root是tkinter中画布的定义位置
canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
Label(root,text="*位移点A-R,温度点A-M,应变点1-44*",font=50).pack()
e1=Label(root,text="选择温度",font=20)
e1.pack()
user_text=Entry()
user_text.pack()
def draw_T():  
    f_plot.clear()
    t =ord(user_text.get()) #用字母表示时
    test_TEM = t-65
    if test_TEM<13:
        col_test_TEM = sh1.col_values(test_TEM)
        x=np.arange(0,1079,1)
        y=np.array(col_test_TEM)                               
        f_plot.set(title='temprature_self',xlabel='time/10min',ylabel='temprature')
        f_plot.plot(x,y)                                                                
        canvs.draw() 
Button(root, text='选择测试点', command=draw_T).pack()
e2=Label(root,text="选择位移",font=20)
e2.pack()
user_text1=Entry()
user_text1.pack()
def draw_D():
    f_plot.clear()
    d =ord(user_text1.get())#用字母表示时
    test_VD = d-65
    if test_VD<18:
        col_test_VD = sh1.col_values(test_VD)
        x=np.arange(0,1079,1)
        y=np.array(col_test_VD)
        f_plot.set(title='ver_d_self',xlabel='time/10min',ylabel='ver_d')
        f_plot.plot(x,y)
        canvs.draw()
Button(root,text='选择测试点',command=draw_D).pack()
e3=Label(root,text="选择应变",font=20)
e3.pack()
user_text2=Entry()
user_text2.pack()
def draw_Y():
    f_plot.clear()
    #y = ord(var.get())  #用字母表示时
    if user_text2.get().isdigit():
        test_YB = int(user_text2.get())-1
    if test_YB<44:
        col_test_YB = sh2.col_values(test_YB)
        x=np.arange(0,1079,1)
        y=np.array(col_test_YB)
        f_plot.set(title='YB_self',xlabel='time/10min',ylabel='YingBian')
        f_plot.plot(x,y)
        canvs.draw()
Button(root, text='选择测试点',command=draw_Y).pack()
root.mainloop()