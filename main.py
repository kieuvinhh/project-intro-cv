import argparse
import random
import time
import cv2
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import os
import PIL
from PIL import Image, ImageTk

root = tk.Tk()
root.title('Selective search')
root.iconbitmap('logo-uit.ico')
root.geometry('900x600')
root.configure(bg='white')


def select_file():
    filetypes = (
        ('', '*.jpg'),
        (' ', '*.png'),
        ('  ', '*.bmp'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.curdir,
        filetypes=filetypes)
    return filename


def resize_Img(img,nrow, ncol):
    scale_row = 326 / nrow
    scale_col = 490 / ncol
    width = int(img.shape[1] * scale_row)
    height = int(img.shape[0] * scale_col)
    img_n = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    return img_n


def Open():
    global img_root
    url_img = select_file()
    img_root = cv2.imread(url_img)
    nrow, ncol, nchl = img_root.shape
    if nrow > 326 or ncol > 490:
        img_root = resize_Img(img_root, nrow, ncol)
    img_temp = cv2.cvtColor(img_root, cv2.COLOR_BGR2RGB)
    img_temp = Image.fromarray(img_temp)
    img1 = ImageTk.PhotoImage(img_temp)
    lbl_image_root.configure(image=img1)
    lbl_image_root.image = img1


def processing():
    btn_open['state'] = DISABLED
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(img_root)
    method = input_entry.get()
    if method == "fast":
        print("[INFO] using *fast* selective search")
        ss.switchToSelectiveSearchFast()
    else:
        print("[INFO] using *quality* selective search")
        ss.switchToSelectiveSearchQuality()
    start = time.time()
    rects = ss.process()
    end = time.time()
    # show how along selective search took to run along with the total
    # number of returned region proposals
    print("[INFO] selective search took {:.4f} seconds".format(end - start))
    print("[INFO] {} total region proposals".format(len(rects)))
    # loop over the region proposals in chunks (so we can better
    # visualize them)
    for i in range(0, len(rects), 100):
        # clone the original image so we can draw on it
        output = img_root.copy()
        # loop over the current subset of region proposals
        for (x, y, w, h) in rects[i:i + 100]:
            # draw the region proposal bounding box on the image
            color = [random.randint(0, 255) for j in range(0, 3)]
            cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        output = Image.fromarray(output)
        output = ImageTk.PhotoImage(output)
        lbl_img_res.configure(image=output)
        lbl_img_res.image = output
        lbl_img_res.update()
        print('Processing')
        time.sleep(2)

    print('end')
    showinfo('Your process is done', 'If result does not satisfied, please try a gain with "Quality mode"')
    btn_open['state'] = NORMAL


btn_open = Button(root, text='Open', font=('Arial', 10), command=Open, bg='white', fg='black', borderwidth=2)
btn_open.place(anchor=SE, x=250, y=100, width=50)

btn_kmean = Button(root, text='Processing', font=('Arial', 10), command=processing, bg='white')
btn_kmean.place(anchor=SE, x=380, y=100, width=100)

lbl_method = Label(root, text='Method: ', font=('Arial', 10), bg='white')
lbl_method.place(anchor=SE, x=470, y=98)

input_entry = Entry(root, highlightthickness=1)
input_entry.configure(highlightbackground='black')
input_entry.place(anchor=SE, x=600, y=97)

lbl_image_root = Label(root, bg='white')
lbl_image_root.place(anchor=E, x=600, y=300)

lbl_img_res = Label(root, bg='white')
lbl_img_res.place(anchor=E, x=1200, y=300)

root.mainloop()
