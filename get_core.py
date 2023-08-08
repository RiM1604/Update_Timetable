from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Path_to_driver="chromedriver.exe"

# wd= webdriver.Chrome()
# url="https://erp.iitkgp.ac.in/ERPWebServices/curricula/CurriculaSubjectsList.jsp?stuType=UG&splCode=CS"
# wd.get(url)
# page_content= wd.page_source
# output_filepath="core_page_content.txt"

# with open(output_filepath,"w",encoding="utf-8") as f:
#     f.write(page_content)

# wd.quit()

with open("core_page_content.txt","r", encoding="utf-8") as f:
    content=f.read()

soup=BeautifulSoup(content,"html.parser")
target_style="background-color: white"
target_attr={"style":target_style,"nowrap":""}

target_tag=soup.find_all("tr")

data=[]
for row in target_tag:
    target_content=row.find_all("td",attrs=target_attr)
    temp=[item.get_text() for item in target_content]
    data.append(temp)
# print(data)
processed_data=[]
for i in range(len(data)):
    if(len(data[i])==0):
        continue
    elif (data[i][2]==""):
        continue
    else:
        processed_data.append(data[i])

def clean(text):
    cleaned_text=""
    for i in range(len(text)):
        if(text[i]==" "):
            continue
        else:
            cleaned_text= cleaned_text+text[i]
    return cleaned_text

required_data=[]
for item in processed_data:
    sub_arr=[]
    for i in range(len(item)):
        if i>=2:
            cleaned_item=clean(item[i])
            sub_arr.append(cleaned_item)
    required_data.append(sub_arr)

# print(required_data)

feature={
    "code":0,
    "name":1,
    "LTP":2,
    "credit":3,
}

# for item in required_data:
#     print(item[feature["code"]])
