import tkinter as tk
from PIL import Image,ImageTk
import back2,related
def back():
    root1 = tk.Tk()
    root1.title('USTB关联规则挖掘可视化系统')
    canvas = tk.Canvas(root1,width = 800,height = 470,bg = 'black')
    image = Image.open("back.jpg")  
    im = ImageTk.PhotoImage(image)  
    canvas.create_image(400,235,image = im)
    canvas.pack()
    tk.Button(root1, text='************▂▃▅▆▇▇▇▇ Apriori关联挖掘 ▇▇▇▇▆▅▃▂************', font=12,
              height=2, command=related.related).pack(fill='both')
    root1.mainloop()