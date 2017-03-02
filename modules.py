# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:50:49 2017

@author: Dylan
"""
import se, random, time
import pandas as pd

def craigslist(driver,instructions):
    
    from selenium import webdriver
    c = webdriver.Chrome(driver)
    c.implicitly_wait(10)
    df = pd.read_csv(instructions)
    x=0
    login=[]
    for each in df.iat[0,5].split(';'):
        login.append(each)
    for _ in range(df.shape[0]):
        location = df.iat[x,0]
        for _ in range(df.shape[1]):
            category = df.iat[x,1]
            p_code = df.iat[x,3]
            body = df.iat[x,2]
            se.browse("https://"+location+".craigslist.org/search/"+category,c)
            se.grab("""//*[@id="page-top"]/header/div/ul[1]/li[1]/a""","click",c)
            se.grab("""/html/body/article/section/form/ul/li[10]/label/span[2]""","click",c)
            se.grab("""/html/body/article/section/form/ul/li[10]/label/span[2]""","click",c)
            se.keys("""//*[@id="inputEmailHandle"]""",str(login[0]),c)
            se.keys("""//*[@id="inputPassword"]""",str(login[1]+"\n"),c)
            
            try:
                se.grab("""/html/body/article/section/form/ul/li[1]/label/input""","click",c)
            except:
                with open("error.log", 'w') as error_log:
                    error_log.write(" [!] No sublocation found, continuing without one for "+location+".\n")
                error_log.close()
            
            se.keys("""//*[@id="PostingTitle"]""",str(df.iat[random.randint(0,range(df.shape[4])),4]),c)
            se.keys("""//*[@id="postal_code"]""",p_code,c)
            se.keys("""//*[@id="PostingBody"]""",body,c)
            se.grab("""//*[@id="wantamap"]""","click",c)
            se.grab("""/html/body/article/section/form/button""","click",c)
            se.grab("""//*[@id="publish_top"]/button""","click",c)
            x+=1
            time.sleep(600)