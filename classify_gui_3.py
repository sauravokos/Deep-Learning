import numpy as np
import tkinter as tk

from keras import applications as ap
#from keras_squeezenet import SqueezeNet
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing import image
from PIL import Image,ImageTk

import os

model = ap.VGG19(weights='imagenet')

class ImageClassifyer(tk.Frame):


    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.v = tk.IntVar()
        self.v.set(1)

        self.root = parent
        self.root.wm_title("Classify Image")   
        src = "./images/"

        self.list_images = []
        for d in os.listdir(src):
            self.list_images.append(d)

        self.frame1 = tk.Frame(self.root, width=500, height=400, bd=2)
        self.frame1.grid(row=1, column=0)
        self.frame2 = tk.Frame(self.root, width=500, height=400, bd=2)
        self.frame2.grid(row=1, column=1)
        self.frame3 = tk.Frame(self.root, width=500, height=10, bd=2)
        self.frame3.grid(row=2, column=1)

        self.cv1 = tk.Canvas(self.frame1, height=390, width=490, background="white", bd=1, relief=tk.RAISED)
        self.cv1.grid(row=1,column=0)
        self.cv2 = tk.Canvas(self.frame2, height=390, width=490, bd=2, relief=tk.SUNKEN)
        self.cv2.grid(row=1,column=0)

        claButton = tk.Button(self.root, text='Classify', height=2, width=10, command=self.classify_obj)
        claButton.grid(row=0, column=1, padx=2, pady=2)
        broButton = tk.Button(self.root, text='Next', height=2, width=8, command = self.next_image)
        broButton.grid(row=0, column=0, padx=2, pady=2)

        label1 = tk.Label(self.frame3, text="Is the deduction...")
        label1.grid(row=0, column=0)

        radButton1 = tk.Radiobutton(self.frame3, text="Correct", variable=self.v, value=1, indicatoron=0)
        radButton1.grid(row=1, column=0)
        radButton2 = tk.Radiobutton(self.frame3, text="Incorrect", variable=self.v, value=0, indicatoron=0)
        radButton2.grid(row=1, column=1)

        self.counter = 0
        self.max_count = len(self.list_images)-1
        self.next_image()

    def classify_obj(self):

        self.cv2.delete("all")
        imag = image.load_img("{}{}".format("./images/", self.list_images[self.counter-1]), target_size=(224, 224))
        x = image.img_to_array(imag)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        co = 0
        preds = model.predict(x)
        all_results = decode_predictions(preds)
        for results in all_results:
            for result in results:
                co += 5
                self.cv2.create_text(10, 5*co, fill="darkblue", font="Arial 16", text='Probability of %0.2f%% => %s' % (100*result[2], result[1]), anchor=tk.NW)
                

    def next_image(self):

        #print(self.v.get())
        self.cv2.delete("all")
        if self.counter+1 > self.max_count:
            print("No more images in folder")
        else:
            im = Image.open("{}{}".format("./images/", self.list_images[self.counter]))
            if (490-im.size[0])<(390-im.size[1]):
                width = 490
                height = width*im.size[1]/im.size[0]
                self.next_step(height, width)
            else:
                height = 390
                width = height*im.size[0]/im.size[1]
                self.next_step(height, width)

    def next_step(self, height, width):

        self.v.set(1)        
        self.im = Image.open("{}{}".format("./images/", self.list_images[self.counter]))
        self.im.thumbnail((width, height), Image.ANTIALIAS)
        #self.root.photo = ImageTk.PhotoImage(self.im)
        self.photo = ImageTk.PhotoImage(self.im)

        if self.counter == 0:
            self.cv1.create_image(0, 0, anchor = 'nw', image = self.photo)

        else:
            self.im.thumbnail((width, height), Image.ANTIALIAS)
            self.cv1.delete("all")
            self.cv1.create_image(0, 0, anchor = 'nw', image = self.photo)
        self.counter += 1
        #print(self.counter)


if __name__ == "__main__":
    
    root = tk.Tk() 
    ClassiApp = ImageClassifyer(root)
    tk.mainloop()
