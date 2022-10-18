import tkinter as tk1
from PIL import Image,ImageTk
import back2,related
def back():
    root1 = tk1.Tk()
    root1.title('桥梁监测信息关联分析可视化系统')
    canvas = tk1.Canvas(root1,width = 800,height = 470,bg = 'black')  
    image = Image.open("back.jpg")  
    im = ImageTk.PhotoImage(image)  
    canvas.create_image(400,235,image = im)
    canvas.pack()
    #tk1.Button(root1,text ='****************▂▃▅▆▇▇▇▇    数据可视化（周期估算）   ▇▇▇▇▆▅▃▂****************',font=12,height=2,command=back2.back2).pack(fill='both')
    tk1.Button(root1,text ='****************▂▃▅▆▇▇▇▇ 传感器的相关计算（相关系数）▇▇▇▇▆▅▃▂****************',font=12,height=2,command=related.related).pack(fill='both')
    root1.mainloop()