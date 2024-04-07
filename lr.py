# 创建tkinter窗口
import tkinter as tk
from tkinter import StringVar, Entry,Label,messagebox
from mdles.models import session, User, Dk
from config.database import Session
from face import facelr
from mdles.models import User
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
root = tk.Tk()
root.title("User Input Form")
root.geometry("400x300")
# 创建输入框变量
name_var = StringVar()
ename_var = StringVar()
money_var = StringVar()
#创建标题
name_label=ttk.Label(root,text="名字",width=10,bootstyle="info")
ename_label=ttk.Label(root,text="英文名字",width=10,bootstyle="info")
money_label=ttk.Label(root,text="工资",width=10,bootstyle="info")
# 创建输入框
name_entry = ttk.Entry(root, textvariable=name_var, width=20 ,bootstyle="danger")
ename_entry = ttk.Entry(root, textvariable=ename_var, width=20,bootstyle="danger")
money_entry = ttk.Entry(root, textvariable=money_var, width=20,bootstyle="danger")

# 布局输入框
name_label.pack(padx=0)
name_entry.pack(padx=50)
ename_label.pack(padx=0)
ename_entry.pack(padx=50)
money_label.pack(padx=0)
money_entry.pack(padx=50)

# 提交按钮
# from face import facelr
def submit_user():


    new_user = User(
        name=name_var.get(),
        ename=ename_var.get(),
        money=int(money_var.get())
    )
    session = Session()
    facename = session.query(User).filter(User.name == name_var.get()).first()
    if facename==None:
        re = facelr(ename_var.get())
        print("re", re)
        session.add(new_user)
        session.commit()
        session.close()
    else:
        messagebox.showinfo("此人已经录入")

submit_button = tk.Button(root, text="人脸录制", command=submit_user)
submit_button.pack(pady=10)

# 运行tkinter窗口
root.mainloop()