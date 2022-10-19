import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
import time
import requests
from lxml import etree
from tkinter import filedialog


class House:
    '''获得一个二手房信息的App'''

    def __init__(self, master):
        self.df_c = ['title', 'layout', 'information', 'house_name', 'address', 'total_price', 'sigal_price', 'link']
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.label1 = tk.Label(master, text='请输入城市名字拼音缩写：', font=('华文行楷', 12))
        self.label1.grid()  # grid是网格布局
        self.entry1 = tk.Entry(master, textvariable=self.var1, font=('Arial', 14), width=65)
        self.entry1.grid(row=0, column=1)

        self.button1 = tk.Button(master, text='查询', font=('微软雅黑', 12), command=self.frist)
        self.button1.grid(row=0, column=2)
        self.entry2 = tk.Entry(master, textvariable=self.var2, font=('Arial', 14), width=87)
        self.entry2.grid(row=1, columnspan=3)
        self.tree1 = ttk.Treeview(
            master,  #
            height=15,  # 表格显示的行数
            columns=self.df_c,  # 显示的列
            show='headings',  # 隐藏首列
        )
        for x in self.df_c:
            self.tree1.heading(x, text=x)
            self.tree1.column(x, width=120)
        self.tree1.grid(row=2, columnspan=3)  # columnspan=3合并单元格，横跨3列
        self.button2 = tk.Button(master, text='上一页', font=('微软雅黑', 12), command=self.beforpage)
        self.button2.grid(row=3, column=0)
        self.button3 = tk.Button(master, text='下一页', font=('微软雅黑', 12), command=self.nextpage)
        self.button3.grid(row=3, column=1)
        self.button4 = tk.Button(master, text='保存数据', font=('微软雅黑', 12), command=self.save)
        self.button4.grid(row=3, column=2)

    def get_data(self, pages):
        city = self.entry1.get()
        if city:

            url = 'https://' + city + '.58.com/ershoufang/p' + str(
                pages) + '/?PGTID=0d200001-0091-98e1-df4d-3bd2817e0cfe&ClickID=1'
            self.var2.set(url)
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

            }

            html = requests.get(url=url, headers=headers).content.decode('utf-8')

            # print(html)
            data = etree.HTML(html)
            lists = data.xpath('//section[@class="list"]/div[@class="property"]')
            # print(lists)
            titles = []
            layouts = []
            information = []
            names = []
            adds = []
            total_prices = []
            sigal_prices = []
            links = []
            for lis in lists:
                # 获得标题title
                title = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-content-detail"]/div[@class="property-content-title"]/h3/@title')[
                    0]
                # title = lis.xpath('./a/@href')
                # 得到布局la
                layout = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-content-detail"]/section/div[@class="property-content-info"]/p[@class="property-content-info-text property-content-info-attribute"]/span/text()')
                la = ''
                for lay in layout:
                    la = la + lay
                # 得到布局la
                ############################
                # 得到面积等信息head
                total = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-content-detail"]/section/div[@class="property-content-info"]/p[@class="property-content-info-text"]/text()')
                head = ''
                dou = ','
                for to in total:
                    head = head + str(to).strip() + dou
                # 得到面积等信息head
                ################################
                # 得到小区名字name
                name = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-content-detail"]/section/div[@class="property-content-info property-content-info-comm"]/p[@class="property-content-info-comm-name"]/text()')[
                    0]
                # 得到地址add
                address = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-content-detail"]/section/div[@class="property-content-info property-content-info-comm"]/p[@class="property-content-info-comm-address"]/span/text()')
                add = ''
                ress = ','
                for ad in address:
                    add = add + ad + ress
                # 得到地址add
                ##########################
                # 得到总价to_price
                total_price = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-price"]/p[@class="property-price-total"]/span/text()')
                to_price = ''
                for totle in total_price:
                    to_price = to_price + totle
                # 得到总价to_price
                ##########################
                # 得到总价si_price
                sigal_price = lis.xpath(
                    './a/div[@class="property-content"]/div[@class="property-price"]/p[@class="property-price-average"]/text()')[
                    0]
                # 得到房产链接link
                link = lis.xpath('./a/@href')[0]
                # 将上面信息添加到列表中
                titles.append(title)
                layouts.append(la)
                information.append(head)
                names.append(name)
                adds.append(add)
                total_prices.append(to_price)
                sigal_prices.append(sigal_price)
                links.append(link)

            data = pd.DataFrame([titles, layouts, information, names, adds, total_prices, sigal_prices, links]).T
            data.columns = ['title', 'layout', 'information', 'house_name', 'address', 'total_price', 'sigal_price',
                            'link']
            return data
        else:
            messagebox.showinfo(title='错误信息', message='请输入内容')

    def show(self, page):
        for row in self.tree1.get_children():
            self.tree1.delete(row)
        self.df = self.get_data(page)
        # self.df_col = self.df.columns.tolist()
        # self.tree1['columns'] = self.df_col
        # for x in self.df_col:
        #     self.tree1.heading(x, text = x)
        #     self.tree1.column(x, width=100)
        # 在treeview中显示dataframe数据
        for i in range(len(self.df)):
            self.tree1.insert('', i, values=self.df.iloc[i, :].tolist())

    def frist(self):
        self.show(1)

    def nextpage(self):
        url = self.entry2.get()  # 获取entry2中字符串
        b = int(url.split('ershoufang/p')[1].split('/')[0]) + 1  # 将字符串分解获得第几页进行+1处理
        if b <= 80:
            self.show(b)
        else:
            messagebox.showwarning(title='错误信息', message='已经是最后一页了')

    def beforpage(self):
        url = self.entry2.get()  # 获取entry2中字符串
        b = int(url.split('ershoufang/p')[1].split('/')[0]) - 1  # 将字符串分解获得第几页进行+1处理
        if b >= 1:
            self.show(b)
        else:
            messagebox.showwarning(title='错误信息', message='已经没有上一页了')

    def save(self):
        try:
            savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            self.df.to_excel(savefile + ".xlsx", index=False, sheet_name="Results")

        except Exception as e:
            messagebox.showerror(title='错误信息', message=str(e))


root = tk.Tk()
root.title('FE_city二手房信息')
# root.iconbitmap('fa.ico') #设置左上角小图标
root.geometry('998x432+200+100')
root.resizable(0, 0)  # 设置窗口不可变
House(root)
root.mainloop()