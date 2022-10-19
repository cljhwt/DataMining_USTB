# -*- coding: utf-8 -*-
import matplotlib
import subprocess
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import tkinter as tk
from tkinter import ttk
import xlrd
import xlwt
import tkinter.messagebox as messagebox
import pandas as pd
# 导入关联规则的包，输出频繁项集和关联规则
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def related():
    data = pd.read_csv('./Market_Basket_Optimisation.csv', header=None)
    root2 = Tk()
    root2.title("数据可视化")
    root2.geometry("600x400")
    df_c=['antecedents', 'consequents', 'lift', 'confidence', 'support']

    tree1 = ttk.Treeview(
        root2,  #
        height=15,  # 表格显示的行数
        columns=df_c,  # 显示的列
        show='headings',  # 隐藏首列
    )
    for x in df_c:
        tree1.heading(x, text=x)
        tree1.column(x, width=120)
    tree1.grid(row=1, columnspan=3)  # columnspan=3合并单元格，横跨3列
    # 复选框
    #check1.grid(column=0, row=4, sticky=W)       # sticky=tk.W  当该列中其他行或该行中的其他列的某一个功能拉长这列的宽度或高度时，设定该值可以保证本行保持左对齐，N：北/上对齐  S：南/下对齐  W：西/左对齐  E：东/右对齐

    def apr():
        # 将原始数据做数据清洗，剔除空值，将数据转成文本str格式
        corpus = pd.DataFrame(columns=['items'])
        for row in range(data.shape[0]):
            tmp = [i for i in data.iloc[row, :].values if str(i) != 'nan']
            corpus.loc[row, 'items'] = ','.join(tmp)
        # print(corpus)

        # 将items进行multi-hot
        corpus = corpus['items'].str.get_dummies(sep=',')
        # print(corpus)

        # 此处设置最小支持度为0.02，可以根据需求进行调参
        frequent_itemsets = apriori(corpus, min_support=0.05, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.5)

        # 按照提升度进行排序展示
        rules_lift_rank = rules.sort_values(by=['lift'], ascending=False)
        print(rules_lift_rank)

        # 按照置信度进行排序展示
        rules_confidence_rank = rules.sort_values(by=['confidence'], ascending=False)
        print(rules_confidence_rank)

        # 按照支持度（k=2）进行排序展示
        rules_support_rank = rules.sort_values(by=['support'], ascending=False)
        print(rules_support_rank)

        table=rules[df_c]
        table['antecedents'] = table['antecedents'].map(lambda x: str(x)[12:-3])
        table['consequents'] = table['consequents'].map(lambda x: str(x)[12:-3])
        table['lift'] = table['lift'].map(lambda x: round(x,4))
        table['confidence'] = table['confidence'].map(lambda x: round(x, 4))
        table['support'] = table['support'].map(lambda x: round(x, 4))
        for i in range(len(table)):
            tree1.insert('', i, values=table.iloc[i, :].tolist())

    button3 = tk.Button(root2,text='查询', font=('微软雅黑', 12), command=apr)
    button3.grid(row=3, column=1)
    #check2.grid(column=1, row=4, sticky=W)
    root2.mainloop()