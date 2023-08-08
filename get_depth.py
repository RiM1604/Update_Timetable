from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Path_to_driver="chromedriver.exe"

# wd= webdriver.Chrome()
# url="https://erp.iitkgp.ac.in/ERPWebServices/curricula/CurriculaElectiveList.jsp?stuType=UG&splCode=CS&semno=5&curr_type=OLD&sub_type=ELECTIVE-I(MATH)"
# wd.get(url)
# page_content= wd.page_source
# output_filepath="page_content.txt"

# with open(output_filepath,"w",encoding="utf-8") as f:
#     f.write(page_content)

# wd.quit()


with open('page_content.txt','r', encoding="utf-8") as f:
    content=f.read()

soup=BeautifulSoup(content,'html.parser')
target_style = "background-color: white"
target_attributes = {"style": target_style, "nowrap": ""}

# Use find_all method to find elements with the specified attributes
table_rows=soup.find_all("tr")
# elements = soup.find_all("td", attrs=target_attributes)
data=[]
for row in table_rows:
    table_data=row.find_all("td",attrs=target_attributes)
    subject_info=[data.get_text() for data in table_data]
    data.append(subject_info)
processed_data=[]
for i in range(len(data)):
    if(len(data[i])==0):
        continue
    else:
       processed_data.append(data[i]) 
    # print(data[i])
# print(processed_data)

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
    sub_list=[]
    for i in range(len(item)):
        if i>=1:
            cleaned_item=clean(item[i])
            sub_list.append(cleaned_item)
    required_data.append(sub_list)




# print(required_data)
feature={
    "code":0,
    "name":1,
    "LTP":2,
    "credits":3
}

# for item in required_data:
#     print(item[feature["code"]])


