import cv2
import numpy as np 
from PIL import Image
import glob
import os
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#ファイルリスト取得
filelist=glob.glob("./data/*.jpg")
filelist=sorted(filelist,key=natural_keys)
print(filelist)
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

images[0].save("output.gif",save_all=True, append_images=images[1:], optimize=False, loop=0)

