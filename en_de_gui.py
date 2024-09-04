# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import aes_en_de, rsa_en_de

window = tk.Tk()
X_MAX = window.winfo_screenwidth()//2 + 300
H_MAX = window.winfo_screenheight()//2
WINDOWS = str(X_MAX) + "x" + str(H_MAX)
LEFT = 20
TOP = 10
FONT_SIZE = 10


def set_windows():
    window.title("加解密工具")
    window.geometry(WINDOWS)

    menu = tk.Menu(window)
    window.config(menu=menu)
    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="exit", command=window.quit)


set_windows()

l1 = tk.Frame(window, borderwidth="1", width=X_MAX, height=H_MAX//4)
l1.keys()
for i in l1.winfo_children():
    i.getvar("text")
    i.winfo_name()
l1.place(x=0, y=0)
l1.propagate(0)


l2 = tk.Frame(window, borderwidth="1", width=X_MAX, height=H_MAX//4)
l2.place(x=0, y=H_MAX//4)
l2.propagate(0)


l3 = tk.Frame(window, borderwidth="1", width=X_MAX, height=H_MAX//4)
l3.place(x=0, y=H_MAX//2)
l3.propagate(0)


def base64_gui():
    pass


"""
var = tk.StringVar()
# var1 = tk.IntVar()
var.set("en")


def select_var():
    messagebox.showinfo(message=var.get())


r1 = tk.Radiobutton(window, text='密文', variable=var, value="en", command=select_var, font=('Arial', FONT_SIZE)).place(x=LEFT, y=TOP)
r2 = tk.Radiobutton(window, text='明文', variable=var, value="de", command=select_var, font=('Arial', FONT_SIZE)).place(x=LEFT, y=TOP+20)
"""
tk.Label(l1, text="明文").place(x=LEFT+25, y=H_MAX//4//2-70//2)
tk.Label(l1, text="或").place(x=LEFT+35, y=H_MAX//4//2-25//2)
tk.Label(l1, text="密文").place(x=LEFT+25, y=H_MAX//4//2+10)
e1 = tk.Text(l1, height=4, width=130, show=None, font=('Arial', FONT_SIZE))


member = tk.StringVar()
lb_en_method = tk.Label(l2, text="加密方式").place(x=LEFT, y=H_MAX//4//2-H_MAX//4//2//4)
def get_combobox(event):
    if member.get() == "RSA":
        t = get_rsa_windows()
        t.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2)
        t.propagate(0)
        get_aes_windows("cancel")
    if member.get() == "AES":
        f = get_aes_windows()
        f.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2 // 4)
        f.propagate(0)
        get_rsa_windows("cancel")


# 创建下拉选框
member_chosen = ttk.Combobox(l2, width=8, textvariable=member, state='readonly')#postcommand=get_combobox)
member_chosen['values'] = ("请选择", "RSA", "AES")     # 设置下拉列表的值
# member_chosen.place(x=LEFT + 60, y=110)      # 设置其在界面中出现的位置  column代表列   row 代表行
member_chosen.place(x=LEFT+60, y=H_MAX//4//2-H_MAX//4//2//4)      # 设置其在界面中出现的位置  column代表列   row 代表行
member_chosen.current(0)
member_chosen.bind("<<ComboboxSelected>>", get_combobox)


# get_aes_windows element
f = tk.Frame(l2, borderwidth="1", width=750, height=20)
tk.Label(f, text="iv").place(x=0, y=0)
iv = tk.Entry(f).place(x=20, y=0)
tk.Label(f, text="key").place(x=170, y=0)
key = tk.Entry(f).place(x=200, y=0)


# pad method
padding = tk.Label(f, text="pad").place(x=350, y=0)
pad_method = tk.StringVar()
model_chosen = ttk.Combobox(f, width=12, textvariable=pad_method, state="readonly")
model_chosen['values'] = ("zeropadding", "pkcs5padding", "pkcs7padding", "iso10126")  # 设置下拉列表的值
model_chosen.place(x=385, y=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
model_chosen.current(0)

# block size
size = tk.Label(f, text="size").place(x=500, y=0)
block_size = tk.StringVar()
model_chosen = ttk.Combobox(f, width=4, textvariable=block_size, state="readonly")
model_chosen['values'] = ("128", "192", "256")  # 设置下拉列表的值
model_chosen.place(x=535, y=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
model_chosen.current(0)

#
method = tk.Label(f, text="method").place(x=600, y=0)
model = tk.StringVar()
model_chosen = ttk.Combobox(f, width=8, textvariable=model, state="readonly")
model_chosen['values'] = ("请选择", "CBC", "ECB")  # 设置下拉列表的值
model_chosen.place(x=660, y=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
model_chosen.current(0)
# iv = tk.Entry(f)
def get_aes_windows(active="active"):
    global f
    if active == "cancel":
        f.place_forget()
        # f.destroy()
    else:
        return f
        # f.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2 // 4)
        # # f.place(x=LEFT + 150, y=110)
        # f.propagate(0)


# get_rsa_windows element
t = tk.Frame(l2, borderwidth="1", width=720, height=150)
secret_key = tk.Label(t, text="secret key").place(x=0, y=45)
public_private_key = tk.Text(t, height=80, width=440, show=None, font=('Arial', 10)).place(x=70, y=0)
def get_rsa_windows(active="active"):
    global t
    if active == "cancel":
        t.place_forget()
    else:
        return t


def _en_crypto():
    iv, key, pad, method, pub_pri_key= "", "", "", "", ""
    if member.get() == "AES":
        f = get_aes_windows()
        # f.keys()
        for i in f.winfo_children():
            # print(i.winfo_name())

            if i.winfo_name() == "!entry":
                if i.get() == "":
                    messagebox.showinfo(message="iv不能为空")
                    return
                else:
                    iv = i.get()
            if i.winfo_name() == "!entry2":
                if i.get() == "":
                    messagebox.showinfo(message="key不能为空")
                    return
                else:
                    key = i.get()
            if i.winfo_name() == "!combobox":
                if i.get() == "请选择":
                    messagebox.showinfo(message="请选择加密模式")
                    return
                else:
                    pad = i.get()
            if i.winfo_name() == "!combobox2":
                if i.get() == "请选择":
                    messagebox.showinfo(message="请选择加密长度")
                    return
                else:
                    size = i.get()
            if i.winfo_name() == "!combobox3":
                if i.get() == "请选择":
                    messagebox.showinfo(message="请选择加密方法")
                    return
                else:
                    method = i.get()
        return {"m":"AES", "iv": iv, "key": key, "pad": pad, "method":method}
    if member.get() == "RSA":
        t = get_rsa_windows()
        for j in t.winfo_children():
            # print(j.winfo_name())
            if j.winfo_name() == "!text":
                if j.get(0.0, "end") == "\n":
                    messagebox.showinfo(message="公/私钥不能为空")
                    return
                else:
                    pub_pri_key = j.get(0.0, "end")
        return {"m": "RSA", "key": pub_pri_key}


def en_crypto():
    en_de_str = e1.get(0.0, "end")

    if en_de_str != "\n":
        # print(en_de_str)
        pass
    else:
        messagebox.showinfo(message="加解密码数据不能为空")
        return
    a = _en_crypto()
    if not a: return
    if a["m"] == "AES":
        # f.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2 // 4)
        # f.propagate(0)
        e2.delete("1.0", "end")
        aes_obj = aes_en_de.Get_aes()

        if a["method"] == "CBC":
            cbc_en_str = aes_obj.cbc_encrypto(en_de_str, iv=a["iv"], key=a["key"])
            # print(cbc_en_str)
            e2.insert("end", cbc_en_str["msg"])
        if a["method"] == "ECB":
            ecb_en_str = aes_obj.ecb_encrypto(en_de_str, key=a["key"])
            e2.insert("end", ecb_en_str["msg"])

    if a["m"] == "RSA":
        # t.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2 // 2)
        # t.propagate(0)
        e2.delete("0.0", "end")
        rsa_en = rsa_en_de.rsa_encrypt(message=en_de_str, key=a["key"])
        if rsa_en["code"] != 0:
            e2.insert("end", rsa_en["msg"])
        else:
            # messagebox.showinfo(message="公钥或私钥错误")
            messagebox.showinfo(message=rsa_en["msg"])


def de_crypto():
    en_de_str = e1.get(0.0, "end")
    a = _en_crypto()
    if a["m"] == "AES":
        # f.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2 // 4)
        # f.propagate(0)
        e2.delete("1.0", "end")
        aes_obj = aes_en_de.Get_aes()

        if a["method"] == "CBC":
            cbc_en_str = aes_obj.cbc_decrypto(en_de_str, iv=a["iv"], key=a["key"])
            if cbc_en_str["code"] != 0:
                e2.insert("end", cbc_en_str["msg"])
            else:
                messagebox.showinfo(message=cbc_en_str["msg"])
        if a["method"] == "ECB":
            ecb_en_str = aes_obj.ecb_decrypto(en_de_str, key=a["key"])
            if ecb_en_str["code"] != 0:
                e2.insert("end", ecb_en_str["msg"])
            else:
                messagebox.showinfo(message=ecb_en_str["msg"])
    if a["m"] == "RSA":
        # t.place(x=LEFT + 150, y=H_MAX // 4 // 2 - H_MAX // 4 // 2 // 2)
        # t.propagate(0)
        e2.delete("0.0", "end")
        rsa_en = rsa_en_de.rsa_decrypt(message=en_de_str, key=a["key"])
        if rsa_en["code"] != 0:
            e2.insert("end", rsa_en["msg"])
        else:
            # messagebox.showinfo(message="公钥或私钥错误")
            messagebox.showinfo(message=rsa_en["msg"])


b_en = tk.Button(l2, text="加密", command=en_crypto)
b_de = tk.Button(l2, text="解密", command=de_crypto)
b_en.place(x=X_MAX-100, y=H_MAX//4//2-H_MAX//4//2//3)
b_de.place(x=X_MAX-60, y=H_MAX//4//2-H_MAX//4//2//3)


l_result = tk.Label(l3, text="加解密", font=('Arial', 10)).place(x=LEFT, y=TOP+20)
l_result2 = tk.Label(l3, text="结    果", font=('Arial', 10)).place(x=LEFT, y=TOP+50)
e2 = tk.Text(l3, height=4, width=130, show=None, font=('Arial', 10))



e1.place(x=LEFT+60, y=H_MAX//4//2-70//2)
e2.place(x=LEFT+60, y=TOP+10)

window.mainloop()
