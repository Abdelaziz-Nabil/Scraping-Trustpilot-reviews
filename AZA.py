#!/usr/bin/env python
# coding: utf-8

# In[51]:


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv
from time import sleep
import time
import datetime
import os
import ntplib
from time import ctime
import requests
from sys import exit


# In[52]:


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# In[53]:


# selenium
# csv
# time
# datetime
# os
# ntplib
# requests
# sys


# In[54]:


def cookies_get():
    try:
        cookies = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID,"onetrust-accept-btn-handler"))
                )
        cookies.click()
    except:
        pass


# In[55]:


def cardData(element):
    link=element.get_attribute('href')
    card_data=(element.text).split("\n")
    if(len(card_data)==4):
        name=card_data[0]
        reviews=card_data[1].split("reviews · TrustScore")[0]
        TrustScore=card_data[1].split("reviews · TrustScore")[1]
        categories=card_data[2]
        address=card_data[3]
    elif(len(card_data)==3):
        name=card_data[0]
        if("reviews · TrustScore" in card_data[1]):
            reviews=card_data[1].split("reviews · TrustScore")[0]
            TrustScore=card_data[1].split("reviews · TrustScore")[1]
            categories=card_data[2]
            address=''
        else:
            reviews=0
            TrustScore=0
            categories=card_data[1]
            address=card_data[2]
    elif(len(card_data)==2):
        name=card_data[0]
        reviews=0
        TrustScore=0
        categories=card_data[1]
        address=""
    else:
        print(card_data)
        
    row=list()
    row.append(name)
    row.append(link)
    row.append(reviews)
    row.append(TrustScore)
    row.append(categories)
    row.append(address)
    return row


# In[56]:


def get_companys():
    p=True
    headrow2=["company","link","number review","company review","category","address"]
    l=0
    cookies_get()
    with open('companies.csv', 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headrow2)
        while(p==True):
            #elements = driver.find_elements(By.CSS_SELECTOR,".styles_categoryBusinessListWrapper__2H2X5 a").styles_businessUnitCardsContainer__1ggaO a
            try:
                elements = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR,".styles_businessUnitCardsContainer__1ggaO a"))#presence_of_element_located
                        )
            except:
                elements=[]
            for x in elements:
                rowData=cardData(x)
                if rowData not in all_data:
                    writer.writerow(rowData)
                    all_data.append(rowData)
            try:
                next = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,"a.button_large__3HOoE.button_primary__2eJ8_"))#presence_of_element_located
                        )
                next.click()
                sleep(3)
                l=0
                p=True
            except:
                if(l==3):
                    p=False
                else:
                    l+=1
                    sleep(3)
    print("get all companies in this category finished")


# In[57]:


def encode_string(tex):    
    #encode() method
    strencode = tex.encode("ascii", "ignore")

    #decode() method
    strdecode = strencode.decode()

    return strdecode


# In[58]:


def date_n(date):
    try:
        ago=int(date.split(" ")[0])
    except:
        ago=0
    tod = datetime.datetime.now()
    d = datetime.timedelta(days = ago)
    a = tod - d
    da_st=str(a.strftime("%b ::::, %Y")).replace("::::",str(a.day))
    return da_st


# In[59]:


def post_element(element):
    row=list()
    try:
        link=element.find_element(By.CSS_SELECTOR,"a.styles_linkwrapper__39Sdq").get_attribute('href')
    except:
        link=''
    try:
        name=element.find_element(By.CSS_SELECTOR,"div.typography_weight-medium__34H_5").text
        name=encode_string(name)
    except:
        name=''
    try:
        head=element.find_element(By.CSS_SELECTOR,"a.styles_linkwrapper__39Sdq").text
        head=encode_string(head)
    except:
        head=''
        
    try:
        contant=element.find_element(By.CSS_SELECTOR,"p.typography_body__2OHdw").text
        contant=encode_string(contant)
    except:
        contant=''
        
    try:
        n_custrumer=driver.find_element(By.CSS_SELECTOR,"span[data-consumer-reviews-count-typography]").text
        n_custrumer=int(n_custrumer.split("review")[0])
    except:
        n_custrumer=1
        
    try:
        date=(element.find_element(By.CSS_SELECTOR,".typography_typography__23IQz time").text).replace("Updated",'')
        if "," not in date:
            date=date_n(date)
    except:
        date=date_n("0 ")
    try:
        rate=element.find_element(By.CSS_SELECTOR,"section div.styles_reviewHeader__GXO3P").get_attribute('data-service-review-rating')
    except:
        rate=''
    
    row.append(name)
    row.append(n_custrumer)
    row.append(link)
    row.append(head)
    row.append(rate)
    row.append(date)
    row.append(contant)

    return row


# In[60]:


def getreviewscompany(url,writer):    
    sleep(3)
    driver.get(url)
    sleep(3)
    cookies_get()
    company_name=(WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,"span.typography_h1__3CI-9"))#presence_of_element_located
                    )).text
    company_reviews=(WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,"span.typography_h2__1PuBA"))#presence_of_element_located
                    )).text
    company_TrustScore=(WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,".styles_rating__1Xlha p"))#presence_of_element_located
                    )).text
    try:
        button = (driver.current_url)+"?page="
        pages=int((WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a.button_medium__252Ld"))#presence_of_element_located
                    ))[-1].text)+1
    except:
        pages=2
        button=url+"?page="
        
        
        
    for y in range(1,pages):
        try:
            post_all =(WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div article"))#presence_of_element_located
                        ))
        except:
            post_all=[]
            driver.close()
            os._exit(0)
            
        company_link=driver.current_url
        for post in post_all:
            row_post=list()
            row_post=post_element(post)
            row_post.append(company_name)
            row_post.append(company_reviews)
            row_post.append(company_TrustScore)
            row_post.append(company_link)
            writer.writerow(row_post)
        print(y," : ",driver.current_url)
        p=True
        l=0
        if(y+1<pages):
            try:
                driver.get(button+str(y+1))
                sleep(3)
                p=False
                l=0
            except:
                while(p==True):
                    try:
                        next = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR,"a.button_large__3HOoE.button_primary__2eJ8_"))#presence_of_element_located
                                )
                        next.click()
                        sleep(3)
                        l=0
                        p=False
                    except:
                        if(l==5):
                            p=False
                        else:
                            l+=1


# In[61]:


def reviews_get(url_g,b):
    headrow=["user","N reviews","review link","head of review","review","date","text","company","number review","company review","page link"]
    if (b==1):
        with open('all.csv', 'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headrow)
            for data in url_g:
                n_r=int((data[2]).replace(",",''))
                if((n_r)!=0):
                    getreviewscompany(data[1],writer)
    elif(b==2):
        with open('company review.csv', 'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headrow)
            getreviewscompany(url_g,writer)


# In[39]:


print("\npeograme start\n")
try:
    choose=int(input("choose what you want \n1- scrap all category(all companies and reviews for eash company)\n2- scrap reviews for one company\n3- scrap all companies in category\nplease inter (1 or 2 or 3) : "))
except:
    print("\nplease enter correct value 1 , 2 , 3..... try again")
    os._exit(0)

sleep(3)
service = Service('chromedriver.exe')
service.start()

if(choose==1):
    url=input("\nEnter category url : ex: https://www.trustpilot.com/categories/cycle_insurance_company \n")
    driver = webdriver.Chrome()
    sleep(2)
    driver.get(url)
    sleep(2)
    all_data=list()
    get_companys()
    reviews_get(all_data,1)
    driver.close()
elif(choose==2):
    url=input("\nEnter company url : ex: https://www.trustpilot.com/review/insurancehub.com\n")
    driver = webdriver.Chrome()
    all_data=list()
    sleep(2)
    reviews_get(url,2)
    driver.close()
elif(choose==3):
    url=input("\nEnter category url : ex: https://www.trustpilot.com/categories/animal_parks_zoo \n")
    driver = webdriver.Chrome()
    sleep(2)
    driver.get(url)
    sleep(2)
    get_companys()
    driver.close()


# In[ ]:




