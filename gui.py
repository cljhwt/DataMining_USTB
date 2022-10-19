# -*- coding: utf-8 -*-
import sys
import fp
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


class GUI(object):
    # 布局界面
    def __init__(self):
        # 设置初始界面
        self.window = tk.Tk()
        self.window.title('关联规则挖掘系统')
        self.window.geometry('1200x550')
        # 导入文件按钮
        self.botton1 = tk.Button(self.window, text='导入文件', bg='green', fg='white', font=('楷体', 12, 'bold'),
                                 width=8, height=1, command=self.openfile)
        self.botton1.place(x=70, y=60)
        # 标签配置
        tk.Label(self.window, text='最小支持数', bg='light blue', fg='white', font=('楷体', 16, 'bold'),
                 width=10, height=1).place(x=10, y=160)
        tk.Label(self.window, text='最小置信度', bg='light blue', fg='white', font=('楷体', 16, 'bold'),
                 width=10, height=1).place(x=10, y=220)
        # 导入文件内容的输出显示
        tk.Label(self.window, text='导入文件内容如下', font=('楷体', 16, 'bold'), width=16,
                 height=1).place(x=260, y=20)
        # 创建结果显示框
        self.text1 = scrolledtext.ScrolledText(self.window, height=28, width=23, font=('楷体', 13))
        self.text1.place(x=250, y=60)
        self.text1.bind("<Button-1>", self.clear)
        # 各个频繁项集和强关联规则的输出显示
        tk.Label(self.window, text='频繁项集和强关联规则', font=('楷体', 16, 'bold'), width=20, height=1).place(x=700,
                                                                                                                y=20)
        # 创建结果显示框
        # self.text2 = scrolledtext.ScrolledText(self.window, height=28, width=60, font=('楷体', 10))
        # self.text2.place(x=550, y=60)
        # self.text2.bind("<Button-1>", self.clear)
        self.df_c = ['antecedents', 'consequents', 'lift', 'confidence', 'support']
        self.table = ttk.Treeview(
            self.window,  #
            height=10,  # 表格显示的行数
            columns=self.df_c,  # 显示的列
            show='headings',  # 隐藏首列
        )
        self.table.place(x=550, y=60)
        for x in self.df_c:
            self.table.heading(x, text=x)
            self.table.column(x, width=120)
        #        self.text2.bind("<Button-1>",self.run)
        # 显示导入文件的路径
        self.var0 = tk.StringVar()
        self.entry1 = tk.Entry(self.window, show=None, width='25', font=('Arial', 10), textvariable=self.var0)
        self.entry1.place(x=10, y=100)
        # 自行设置最小支持度计数值,默认为0.5
        self.var1 = tk.StringVar()
        self.var1.set('3')
        self.entry2 = tk.Entry(self.window, show=None, width='3', font=('Arial', 16), textvariable=self.var1)
        self.entry2.place(x=180, y=160)
        # 自行设置最小置信度参数值，默认为0.7
        self.var2 = tk.StringVar()
        self.var2.set('0.7')
        self.entry3 = tk.Entry(self.window, show=None, width='3', font=('Arial', 16), textvariable=self.var2)
        self.entry3.place(x=180, y=220)
        # 选择所需算法
        self.btnlist = tk.IntVar()
        self.radiobtn1 = tk.Radiobutton(self.window, variable=self.btnlist, value=0, text='Apriori算法', font=('bold'),
                                        command=self.runApriori)
        self.radiobtn1.place(x=30, y=290)
        self.radiobtn2 = tk.Radiobutton(self.window, variable=self.btnlist, value=1, text='FP-Growth算法',
                                        font=('bold'), command=self.runFPGrowth)
        self.radiobtn2.place(x=30, y=330)
        self.btnlist.set(0)
        # 开始运行按钮
        #        self.btn1=tk.Button(self.window, bg='green',fg='white', text='运行', font=('楷体', 12,'bold'), width=6, height=1, command=self.run)
        #        self.btn1.place(x=80,y=360)
        # 清空页面按钮
        self.btn2 = tk.Button(self.window, bg='green', fg='white', text='清屏', font=('楷体', 12, 'bold'), width=6,
                              height=1)
        self.btn2.place(x=80, y=390)
        self.btn2.bind("<Button-1>", self.clear)
        # 关闭页面按钮
        self.btn3 = tk.Button(self.window, bg='green', fg='white', text='退出', font=('楷体', 12, 'bold'), width=6,
                              height=1)
        self.btn3.place(x=80, y=450)
        self.btn3.bind("<Button-1>", self.close)
        # 主窗口循环显示
        self.window.mainloop()

    # 清空所填内容
    def clear(self, event):
        #       连同导入文件一起删除的话，会影响操作的连贯性,故注释掉
        #        self.entry1.delete(0,tk.END)
        #        self.entry2.delete(0,tk.END)
        #        self.entry3.delete(0,tk.END)
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)

    # 退出系统，对控制台清屏
    def close(self, event):
        e = tk.messagebox.askokcancel('询问', '确定退出系统吗？')
        if e == True:
            exit()
            self.window.destroy()

    def __del__(self):
        # 恢复sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    # 从输入文本框中获取文本并返回数字列表
    def getDataSupport(self):
        entry_num1 = float(self.var1.get())
        return entry_num1

    def getDataConfidence(self):
        entry_num2 = float(self.var2.get())
        return entry_num2

    def openfile(self):
        nameFile = filedialog.askopenfilename(title='打开文件', filetypes=[('csv', '*.csv'), ('txt', '*.txt')])
        self.entry1.insert('insert', nameFile)

    def getnamefile(self):
        namefile = self.var0.get()
        return namefile

    # 读取导入的文件并转化为列表
    def loadDataSet(self):
        nameFile = self.getnamefile()
        with open(nameFile, "r", encoding='utf-8') as myfile:
            data = myfile.read()
            self.text1.insert("0.0", data)
            self.text1.see("end")
            list_result = data.split("\n")  # 以回车符\n分割成单独的行
            length = len(list_result)
            for i in range(length):
                list_result[i] = list_result[i].split(",")  # csv文件中的元素是以逗号分隔的
            return list_result
    def apr(self):
        # 将原始数据做数据清洗，剔除空值，将数据转成文本str格式
        data = pd.read_csv(self.getnamefile(), header=None)
        self.text1.insert("0.0", data.values)
        self.text1.see("end")
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

        rules['antecedents'] = rules['antecedents'].map(lambda x: str(x)[12:-3])
        rules['consequents'] = rules['consequents'].map(lambda x: str(x)[12:-3])
        rules['lift'] = rules['lift'].map(lambda x: round(x,4))
        rules['confidence'] = rules['confidence'].map(lambda x: round(x, 4))
        rules['support'] = rules['support'].map(lambda x: round(x, 4))

        return rules

    def runApriori(self):
        # loadDataSet = self.loadDataSet()
        # C1 = self.createC1(loadDataSet)
        # D = list(map(set, loadDataSet))
        minSupport = self.getDataSupport()
        # L1, suppData0 = self.scanD(D, C1, minSupport)
        # L, suppData = self.apriori(loadDataSet, minSupport)
        minConf = self.getDataConfidence()
        # rules = self.generateRules(L, suppData, minConf)
        rules = self.apr()
        table = rules[self.df_c]
        for i in range(len(table)):
            self.table.insert('', i, values=table.iloc[i, :].tolist())

    def runFPGrowth(self):
        self.text1.delete("1.0", "end")
        self.text2.delete("1.0", "end")
        dataSet = self.loadDataSet()
        frozenDataSet = fp.transfer2FrozenDataSet(dataSet)
        minSupport = self.getDataSupport()
        s = '#######################FP_Growth算法########################\n'
        self.text2.insert('insert', s)
        t = '\nFP树：\n'
        self.text2.insert('insert', t)
        fptree, headPointTable = fp.createFPTree(frozenDataSet, minSupport)
        fptree.disp()
        self.text2.insert('insert', fptree.display())
        frequentPatterns = {}
        prefix = set([])
        fp.mineFPTree(headPointTable, prefix, frequentPatterns, minSupport)
        t1 = '\n频繁项集：\n'
        self.text2.insert('insert', t1)
        t2 = frequentPatterns
        self.text2.insert('insert', t2)
        minConf = self.getDataConfidence()
        rules = []
        fp.rulesGenerator(frequentPatterns, minConf, rules)
        t3 = '\n\n强关联规则：\n'
        self.text2.insert('insert', t3)
        for line in rules:
            r = str(line[0]) + '-->' + str(line[1]) + '置信度：' + str(line[2]) + '\n'
            self.text2.insert('insert', r)

    # 创建集合C1，C1是大小为1的所有候选项集合
    def createC1(self, dataSet):
        C1 = []
        for transaction in dataSet:
            for item in transaction:
                if not [item] in C1:
                    C1.append([item])
        C1.sort()
        return list(map(frozenset, C1))  # 对C1中每个项构建一个不变集合

    # 扫描数据集，返回最频繁项集的支持度supportData
    def scanD(self, D, Ck, minSupport):
        ssCnt = {}
        for tid in D:
            for can in Ck:
                if can.issubset(tid):
                    if can not in ssCnt:
                        ssCnt[can] = 1
                    else:
                        ssCnt[can] += 1
        #        numItems = float(len(D))
        retList = []
        supportData = {}
        for key in ssCnt:
            #            support = ssCnt[key] / numItems #计算所有项集支持度
            support = ssCnt[key]
            if support >= minSupport:
                retList.insert(0, key)
            supportData[key] = support
        return retList, supportData

    # 创建候选项集Ck
    def aprioriGen(self, Lk, k):
        retList = []
        lenLk = len(Lk)
        for i in range(lenLk):  # 前k-2个项相同时，将两个集合合并
            for j in range(i + 1, lenLk):
                L1 = list(Lk[i])[:k - 2]
                L2 = list(Lk[j])[:k - 2]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    retList.append(Lk[i] | Lk[j])
        return retList

    # Apriori算法函数
    def apriori(self, dataSet, minSupport):
        minSupport = self.getDataSupport()
        C1 = self.createC1(dataSet)
        D = list(map(set, dataSet))
        L1, supportData = self.scanD(D, C1, minSupport)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.aprioriGen(L[k - 2], k)
            Lk, supK = self.scanD(D, Ck, minSupport)  # 扫描数据集，从Ck得到Lk
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData

    # 生成关联规则
    def generateRules(self, L, supportData, minConf):
        minConf = self.getDataConfidence()
        bigRuleList = []
        for i in range(1, len(L)):
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                if (i > 1):
                    self.rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
                else:
                    self.calcConf(freqSet, H1, supportData, bigRuleList, minConf)
        return bigRuleList

        # 计算可信度值

    def calcConf(self, freqSet, H, supportData, brl, minConf):
        minConf = self.getDataConfidence()
        prunedH = []
        for conseq in H:
            conf = supportData[freqSet] / supportData[freqSet - conseq]
            if conf >= minConf:
                #                print (freqSet-conseq,'-->',conseq,'conf:',conf)
                brl.append((freqSet - conseq, conseq, conf))
                prunedH.append(conseq)
        return prunedH

    # 从最初的项集中生成更多的关联规则
    def rulesFromConseq(self, freqSet, H, supportData, brl, minConf):
        minConf = self.getDataConfidence()
        m = len(H[0])
        if (len(freqSet) > (m + 1)):
            Hmp1 = self.aprioriGen(H, m + 1)
            Hmp1 = self.calcConf(freqSet, Hmp1, supportData, brl, minConf)
            if (len(Hmp1) > 1):
                self.rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


if __name__ == '__main__':
    GUI()
