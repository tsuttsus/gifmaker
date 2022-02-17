import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from tkinter import messagebox
import threading
import os
import sys
import cv2
import re
import numpy as np 
from PIL import Image
import glob

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def openFolderDialog():
    path=filedialog.askdirectory(initialdir ="./")
    indir.set(path)

def execute():
    #ファイルリスト取得
    filedir=indir.get()
    filelist=glob.glob(filedir+"/*.jpg")
    filelist=sorted(filelist,key=natural_keys)
    
    if len(filelist)==0:
        messagebox.showerror("Error", "画像がディレクトリ内に含まれていません")
        sys.exit(1)

    images=[]
    for f in filelist:
        #画像読込
        img=cv2.imread(f,1)
        #BGR2RGB
        b,g,r=cv2.split(img)
        img=cv2.merge([r,g,b])
        #Pillow変換
        pimg=Image.fromarray(img)
        #画像追加
        images.append(pimg)
    
    try:
        images[0].save("output.gif",save_all=True, append_images=images[1:], optimize=False, loop=0)
    except:
        messagebox.showerror("Error", "画像が保存が出来ませんでした")
    
    messagebox.showinfo("Success","完了しました")
    EditBox1.configure(state='normal') 

def asyncexe():
    #GUI調節
    EditBox1.configure(state='readonly') 
    thread1=threading.Thread(target=execute)
    thread1.setDaemon(True)
    thread1.start()

if __name__=="__main__":
    
    root=tk.Tk()
    root.geometry("430x200")
    root.title('gif maker')
    root.resizable(0,0)

    global indir
    indir=tk.StringVar()

    #入力ディレクトリ
    static=tk.Label(text = u'データディレクトリ')
    static.place(x=20,y=30)
    
    global EditBox1,EditBox2
    EditBox1 = tk.Entry(width=30,textvariable= indir)
    EditBox1.place(x=120,y=30)

    inputbutton = ttk.Button(root,text="選択",command =openFolderDialog).place(x=330,y=28)

    caution=tk.Label(text = u'画像はJPG形式で連番にしてください。')
    caution.place(x=120,y=90)

    global button
    button = ttk.Button(root,text = '実行',command = asyncexe).place(x=175,y=120)

    root.mainloop() 
