#Logic

# crop image into respective columns because column size not changing then use cv2 and HoughLine method to get the outlines of the rows 
# then cut the images into the respective rows and name the rows according to the day
# then use ocr get names and course 
# then match the course number with the course name(maybe do classrooms for even and odd also) 
# then use the images of all rows with the day and create a row for the day (dont forget to include images of columns with no text also to make a table)



import PIL
import cv2
from PIL import Image
import numpy as np
from get_core import required_data as core_courses
from get_depth import required_data as depth_courses
from get_core import feature
import os
import pytesseract
import shutil

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
myconfig=r"--psm 6 --oem 3"

# # # takes columns inputs and cuts them into the rows




def get_code(text):
    code=""
    for i in range(len(text)):
        if(text[i]!="\n"):
            code=code+text[i]
        else:
            break
    return code

def get_room_no(text):
    room_no=""
    for i in range(len(text)):
        while (text[i]!="\n"):
            i=i+1
        i=i+1
        break
    while(i<len(text) and text[i]!="\n"):
        room_no=room_no+text[i]
        i=i+1
    return room_no


def cut_into_rows(input_image_path,output_directory):
    cut_column_with_detected_row_lines(input_image_path,output_directory)

def cut_sep_columns_into_rows(no_of_columns):
    i=1
    while i<=no_of_columns:
        extra_path="column_"+str(i)
        directory="output"
        output_path=os.path.join(directory,extra_path)
        input_path="column"+str(i)+"_img.png"
        if os.path.exists(output_path):
            print("Folder already exists")
        else:
            os.mkdir(output_path)
        cut_into_rows(input_path,output_path)
        i=i+1



def detect_row_lines(input_path):
    try:
        # Load the input image
        image = cv2.imread(input_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection to find the edges
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Detect lines using the Hough Line Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=5)

        # Sort the lines based on their y-coordinates
        lines = sorted(lines, key=lambda x: x[0][1])
        # for line in lines:
        #     print(line[0][1])
        # Extract the y-coordinates of the row lines
        row_lines = [line[0][1] for line in lines]

        return row_lines

    except Exception as e:
        print(f"Error while detecting row lines: {e}")
        return None

def cut_column_with_detected_row_lines(input_path, output_directory):
    try:
        # Detect row lines in the image
        row_lines = detect_row_lines(input_path)
        # print(row_lines)

        if row_lines is None:
            print("Row lines detection failed.")
            return

        # Open the input image
        image = Image.open(input_path)

        # Get the dimensions of the image
        width, height = image.size

        # Cut the image into rows using the detected row lines
        for i in range(len(row_lines) - 1):
            # Get the row line coordinates
            top = row_lines[i]
            bottom = row_lines[i + 1]

            # Crop the row from the column image
            row_image = image.crop((0, top, width, bottom))

            # Save the cropped row image to the output directory
            output_path = output_directory
            extra=str(i + 1)+".png"
            output_path= os.path.join(output_path,extra)
            row_image.save(output_path)

        print(f"{len(row_lines) - 1} rows extracted and saved successfully.")
    except Exception as e:
        print(f"Error while cutting image: {e}")




days={
    1:"monday",
    2:"tuesday",
    3:"wednesday",
    4:"thursday",
    5:"friday",
    6:"idk_what_happened"
}



def same_course(img_before,img_after):




    # image=PIL.Image.open(img_before)
    # image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Apply median blur for denoising
    # gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    # _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply thresholding
    # before_text = pytesseract.image_to_string(Image.fromarray(thresholded_image), config='--psm 6')

    # image=PIL.Image.open(img_after)
    # image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # Apply median blur for denoising
    # gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    # _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # after_text = pytesseract.image_to_string(Image.fromarray(thresholded_image), config='--psm 6')

    
    before_text = pytesseract.image_to_string(PIL.Image.open(img_before),config=myconfig)
    after_text = pytesseract.image_to_string(PIL.Image.open(img_after),config=myconfig)
    before_text=before_text.upper()
    after_text=after_text.upper()
    before_text=get_code(before_text)
    after_text=get_code(after_text)
    if(before_text==after_text and before_text!="" and after_text!=""):
        return True
    else:
        print(before_text,after_text)
        return False
    
#creates cut row images with names as monday etc
def create_cut_images(no_of_columns):
    cut_sep_columns_into_rows(no_of_columns)
    directory="output"
    j=1
    while(j<=no_of_columns):
        extra_path="column_"+str(j)
        path=os.path.join(directory,extra_path)
        j=j+1
        imgs=[file for file in os.listdir(path)]
        # print(type(imgs[0]))
        parts=[]
        for img in imgs:
            split_text=img.split(".png")
            parts.append(int(split_text[0]))
        parts=sorted(parts)
        print(parts)
        i=1
        # print(path)
        while(i<=max(parts)):
            if(i%2==0):
                extra_path2=str(i)+".png"
                filepath=os.path.join(path,extra_path2)
                # print(filepath)
                os.remove(filepath)
                # removing the even numbered images               
            i=i+1
        change_names(path,max(parts))


def change_names(path,no_of_files):
    print("change_names_called")
    day_count=1
    i=1
    while(i<=no_of_files):
        if i<=(no_of_files-2):
            temp_addr2=str(i+2)+".png"
            temp_addr1=str(i)+".png"
            image_before=os.path.join(path,temp_addr1)
            image_after=os.path.join(path,temp_addr2)
            print(image_before)
            print(image_after)
            if same_course(image_before,image_after):
                new_filepath1= os.path.join(path,days[day_count]+"1"+".png")
                new_filepath2=os.path.join(path,days[day_count]+"2"+".png")
                old_filepath1=image_before
                old_filepath2=image_after
                shutil.copy(old_filepath1,new_filepath1)
                shutil.copy(old_filepath2,new_filepath2)
                print(f"same course{i}")
                day_count=day_count+1#increasing the day_name by 1
                i=i+2*2
            else:
                new_filepath= os.path.join(path,days[day_count]+".png")
                day_count=day_count+1
                old_filepath=image_before
                shutil.copy(old_filepath,new_filepath)
                print(f"not same {i}")      
                i=i+2
        else:

            temp_addr3=str(i)+".png"
            addr=os.path.join(path,temp_addr3)
            old_filepath3=addr
            new_filepath3=os.path.join(path,days[day_count]+".png")
            shutil.copy(old_filepath3,new_filepath3)
            break


# cut_sep_columns_into_rows(1)
# create_cut_images(1)
# print(same_course("output\\column_1\\1.png","utput\\column_1\\3.png"))
# text1 = pytesseract.image_to_string(PIL.Image.open("output\\column_1\\1.png"),config=myconfig)
# text1=text1.upper()
# text2 = pytesseract.image_to_string(PIL.Image.open("output\\column_1\\3.png"),config=myconfig)
# text2=text2.upper()
# text2=get_code(text2)
# text1=get_code(text1)
# if text1==text2:
#     print("yes both have the same code")

    
# print(days[1])

# op=os.path.join("output","column_5")
# cut_into_rows("column5_img.png",op)
# create_cut_images()

#setup for ocr

# text = pytesseract.image_to_string(PIL.Image.open("output/column_1/1.png"),config=myconfig)
# text=text.upper()

# code=get_code(text)
# room_no=get_room_no(text)
# print(code)
# print(room_no)

# print(core_courses)
# print(depth_courses)
# print(core_courses)

# print(type(code))

# print(core_courses)
# print(feature["code"])

# if "ritesh"=="ritesh":
#     print("yesdfadf")

# for i in range(len(core_courses)):
#     print(core_courses[i][feature["code"]])

# print(core_courses[35][feature["code"]])
# print(type(core_courses[35][feature["code"]]))
# print(type(code))
# print(code)
# print(core_courses[35][feature["code"]])
# print(core_courses[35][feature["code"]]==code.upper())


# for i in range(len(core_courses)):
#     if(code==core_courses[i][feature["code"]]):
#         print(core_courses[i][feature["name"]])
#         break

cut_sep_columns_into_rows(9)
create_cut_images(9)