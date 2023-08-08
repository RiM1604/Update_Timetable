import cv2
from PIL import Image
import os
import pytesseract
import shutil

# img=Image.open("image.png")

# left,top,right,bottom=89,32,215,400

# imagecrop=img.crop((left,top,right,bottom))

# imagecrop.show()

def save_column_imgs(start,no_of_columns,left,top,right,bottom,add_width):
    i=start
    img=Image.open("image.png")
    # add_height=368
    while(i<=(start+no_of_columns-1)):
        cropped_img=img.crop((left,top,right,bottom))
        img_name="column"+str(i)+"_img.png"
        cropped_img.save(img_name)
        left=left+add_width
        right=right+add_width
        i=i+1
    return i,left,top,right,bottom

#no of columns is the starting point of the column name

i,left,top,right,bottom=save_column_imgs(1,2,87,27,212,392,124)
print(i,left,top,right,bottom)
right=right+17
i,left,top,right,bottom=save_column_imgs(i,2,left,top,right,bottom,142)
print(i,left,top,right,bottom)
right=right-3
i,left,top,right,bottom=save_column_imgs(i,1,left,top,right,bottom,142)
print(i,left,top,right,bottom)
right=right-17
i,left,top,right,bottom=save_column_imgs(i,4,left,top,right,bottom,125)
print(i,left,top,right,bottom)
# i,left,top,right,bottom=save_column_imgs(i,4,left,top,right,bottom,130)
# print(i,left,top,right,bottom)
# # save_column_imgs()