#  -*- coding: utf-8 -*-
import sys
from tkinter import *
import tkinter.filedialog as file
import webbrowser
from datetime import datetime
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import pyperclip
import os
import _tkinter
'''
我是Axtol，一名初中生
喜欢写程序、玩游戏

这个程序是我的第一个公开发表的程序
如果有bug，欢迎指正！

有些地方因为能力有限，实在难以实现地很漂亮，如果有改进建议，欢迎提出！
QQ:107475539
邮箱同上

感谢CSDN提供的部分源代码资源！
'''
big = 12

root = Tk()
root.title("Text editor based on Tcl/Tk Python Edition 1.3")    # 标题
root.state("zoomed")    # 最大化


sb = Scrollbar(root)
sb.place(relx=0.995, rely=0.5, relwidth=0.009, relheight=0.945, anchor=CENTER) # 滚动条


text = Text(root, width=100, height=70, undo=True, exportselection=True, yscrollcommand=sb.set)
text.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.945, anchor=CENTER)   # 文本框


label = Label(root, relief=SUNKEN, height=1, justify=RIGHT, padx=10)
label.place(relx=0.5, rely=0.987, relwidth=0.98, relheight=0.028, anchor=CENTER)


def row_col(ev = None):
    r, c = text.index('insert').split('.')
    label['text'] = " " * 430 + f'row:{r}| column:{c}'
text.event_add('<<REACT>>', *('<Motion>', '<ButtonRelease>', '<KeyPress>', '<KeyRelease>'))
b = text.bind('<<REACT>>', row_col)
row_col()    # 获取坐标

sb.config(command=text.yview)


def save(self=None):  # 保存为.py
    save_file = file.asksaveasfilename(defaultextension=".txt", filetypes=[
        ("TXT", ".txt"), ("Python files", (".py", ".pyw")),],
                                      initialdir=r'C:\Users\Administrator\Desktop')
    if save_file == "":
        pass
    else:
        save_tmp = str(os.path.basename(save_file))
        save_dir = str(os.path.dirname(save_file))
        f = open(str(os.path.join(save_dir, "temp.txt")), "w")
        f.write("#  -*- coding: cp936 -*-\n")
        f.write(text.get(1.0, END))
        f.close()
        o = open(str(os.path.join(save_dir, "temp.txt")), "r")
        s = open(str(os.path.join(save_dir, save_tmp)), "w")
        for i in o:
            s.write(str(i))
        o.close()
        s.close()
        os.remove(str(os.path.join(save_dir, "temp.txt")))


def revoke(self=None):
    text.edit_undo()


def recovery(self=None):
    text.edit_redo()


def new(self=None):
    text.delete(1.0, END)


def open_file(self=None):
    of = file.askopenfilename(defaultextension=".txt", filetypes=[("TXT", ".txt"), ("Python files", (".py", ".pyw"))],
                              initialdir=r'C:\Users\Administrator\Desktop')
    f = open(of, encoding="utf-8")
    text.insert(1.0, f.read())
    f.close()


def ext(self=None):
    root.quit()


def se(self=None):
    top = Toplevel()
    top.title("正则表达式查找")
    Label(top, text="输入要查找的字符：").grid(row=0, column=0)
    get = Entry(top, width=25)
    get.grid(row=0, column=1)
    def But():
        search = re.search(r"".join(get.get()), "".join(text.get(1.0, END)))
        Label(top, text=f"找到啦，在：\n{str(search)}").grid(row=0, column=0)
    Button(top, text="查找", command=But, width=5, height=2).grid(row=0, column=2)


def se_tk(self=None):
    top = Toplevel()
    top.title("Tk默认查找(行/列)")
    pit = Label(top, text="输入查找的字符")
    pit.grid(row=0, column=0)
    get = Entry(top, width=25)
    get.grid(row=0, column=1)
    def ged(text, index):
        return tuple(map(int, str.split(text.index(index), ".")))
    def But():
        res = Toplevel()
        res.title("结果")
        te = Text(res)
        te.grid(row=0, column=0)
        start = 1.0
        while True:
            pos = text.search(get.get(), start, stopindex=END)
            if not pos:
                break
            a = ged(text, pos)
            start = pos + "+1c"
            te.insert(END, "找到啦，在" + str(a) + "\n")

    Button(top, text="查找", command=But, width=5, height=2).grid(row=0, column=2)


def bing(self=None):
    webbrowser.open(r"https://cn.bing.com/?scope=web")


def data_time(self=None):
    now = datetime.now()
    text.insert(INSERT, f"{str(now.year)}年{str(now.month)}月{str(now.day)}日 "
                        f"{str(now.hour)}:{str(now.minute)}:{str(now.second)}.{str(now.microsecond)}\n")


def openByP(self=None):
    f = open(r"save.pyw", "w")
    f.write(f"""#! /usr/bin/env python
#  -*- coding: cp936 -*-
""")
    f.write('''
import sys
message = open("message.err", "w")
stderr = sys.stderr
stdout = sys.stdout
sys.stderr = message
sys.stdout = message
''')
    f.write(text.get(1.0, END) + "\n\n")
    f.write('''
message.close()
sys.stderr = stderr
sys.stdout = stdout
''')
    f.close()
    os.system(f"cd {os.path.dirname(sys.argv[0])}")
    os.system("python save.pyw")
    top = Toplevel()
    top.title("结果打印台")
    te = Text(top)
    te.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
    res = open(r"message.err", "r")
    for i in res:
        if "Traceback (most recent call last):" in i:
            te.tag_config("error", background="yellow", foreground="red")
            te.insert(END, str(i), ("error"))
        else:
            te.insert(END, str(i))
    res.close()
    te.config(state=DISABLED)
    os.remove("message.err")
    os.remove("save.pyw")


def copy(self=None):
    try:
        a = text.selection_get()
    except _tkinter.TclError:
        pyperclip.copy("你在想什么？")
    else:
        pyperclip.copy(str(a))


def pas(self=None):
    spam = pyperclip.paste()
    text.insert(END, str(spam))


def popup(event):
    popMenu.post(event.x_root, event.y_root)


def pack():
    pass

# 右键菜单
popMenu = Menu(root, tearoff=False)
popMenu.add_command(label="复制", command=copy)
popMenu.add_command(label="粘贴", command=pas)
popMenu.add_separator()
popMenu.add_command(label="查找(re)    Ctrl + f", command=se)
popMenu.add_command(label="查找(tk)   shift + f", command=se_tk)
text.bind("<Button-3>", popup)


text.bind("<Control-KeyPress-s>", save)
text.bind("<Control-KeyPress-Z>", revoke)
text.bind("<Control-KeyPress-r>", recovery)
text.bind("<Control-KeyPress-h>", new)
text.bind("<Control-KeyPress-o>", open_file)
text.bind("<Control-Shift-KeyPress-X>", ext)
text.bind("<Control-KeyPress-f>", se)
text.bind("<Control-KeyPress-e>", bing)
text.bind("<KeyPress-F6>", data_time)
text.bind("<KeyPress-F5>", openByP)
text.bind("<Shift-KeyPress-F>", se_tk)


# 菜单
menubar = Menu(root)


fileMenu = Menu(menubar, tearoff=False)
fileMenu.add_command(label="保存                 Ctrl+s", command=save)
fileMenu.add_command(label="打开                 Ctrl+o", command=open_file)
fileMenu.add_command(label="新建                 Ctrl+h", command=new)
fileMenu.add_separator()
fileMenu.add_command(label="退出         Ctrl+shift+x", command=ext)
fileMenu.add_separator()
fileMenu.add_command(label="调试.py文件          F5", command=openByP)
menubar.add_cascade(label="文件", menu=fileMenu)


editMenu = Menu(menubar, tearoff=False)
editMenu.add_command(label="撤销                    Ctrl+z", command=revoke)
editMenu.add_command(label="重做                    Ctrl+r", command=recovery)
editMenu.add_separator()
editMenu.add_command(label="查找[re]   Ctrl+f", command=se)
editMenu.add_command(label="查找[Tk]       Shift+f", command=se_tk)
editMenu.add_command(label="用Bing搜索          Ctrl+e", command=bing)
editMenu.add_separator()
editMenu.add_command(label="时间/日期                  F6", command=data_time)
menubar.add_cascade(label="编辑", menu=editMenu)

root.config(menu=menubar)

# 以下代码非原创

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYG>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)

cdg.tagdefs['MYG'] = {'foreground': '#f02645', 'background': '#FFFFFF'}

# 颜色

cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#0090f0', 'background': '#FFFFFF'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#CC33CC', 'background': '#FFFFFF'}
cdg.tagdefs['STRING'] = {'foreground': '#F67c05', 'background': '#FFFFFF'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#F999FF', 'background': '#FFFFFF'}

ip.Percolator(text).insertfilter(cdg)

# 以下代码原创

Button(root, text="打开", command=open_file, width=10, bg="#00FFff").\
    place(relx=0.031, rely=0.014, anchor=CENTER)
Button(root, text="保存", command=save, width=10, bg="#00FFff").\
    place(relx=0.073, rely=0.014, anchor=CENTER)
Button(root, text="新建", command=new, width=10,  bg="#00FFff"). \
    place(relx=0.114514, rely=0.014, anchor=CENTER)
Button(root, text="复制", command=copy, width=10, bg="#00FFff"). \
    place(relx=0.156, rely=0.014, anchor=CENTER)
Button(root, text="粘贴", command=pas, width=10, bg="#00FFff"). \
    place(relx=0.198, rely=0.014, anchor=CENTER)
Button(root, text="寻找(re)", command=se, width=10, bg="#00FFff"). \
    place(relx=0.2395, rely=0.014, anchor=CENTER)
Button(root, text="寻找(tk)", command=se_tk, width=10, bg="#00FFff"). \
    place(relx=0.281, rely=0.014, anchor=CENTER)
Button(root, text="调试.py文件", command=openByP, width=10, bg="#00FFff"). \
    place(relx=0.323, rely=0.014, anchor=CENTER)


# 侧边工具栏
Button(root, text="r\nu\nn", width=1, height=4, bg="#00ccFF", command=openByP).\
    place(relx=0.0001, rely=0.92, relwidth=0.01)
Button(root, text="s\na\nv\ne", width=1, height=4, bg="#00ccFF", command=save).\
    place(relx=0.0001, rely=0.85, relwidth=0.01)
Button(root, text="P\ny\nt\nh\no\nn\n交\n互\n式\n开\n发\n环\n境", width=1, height=13, bg="#00ccFF").\
    place(relx=0.0001, rely=0.62, relwidth=0.01)


try:
    mainloop()
except AttributeError:
    pass
