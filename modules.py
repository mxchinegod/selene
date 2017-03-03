import se, random, time, os
import pandas as pd
from selenium import webdriver

def log_(msg):
    with open("error.log", 'a') as error_log:
        error_log.write(msg+'\n')
        error_log.close()

def craigslist(driver,instructions):
    
    c = webdriver.Chrome(driver)
    c.implicitly_wait(10)
    df = pd.read_csv(instructions)
    x=0
    login=[]
    for each in str(df.iat[x,5]).split(';'):
        login.append(each)
    for _ in range(df.shape[0]):
        location = df.iat[x,0]
        for _ in range(df.shape[1]):
            category = df.iat[x,1]
            p_code = df.iat[x,3]
            body = df.iat[x,2]
            se.browse("https://"+str(location)+".craigslist.org/",c)
            se.grab("""//*[@id="post"]""","click",c,"xpath")
            se.grab("""/html/body/article/section/form/ul/li[10]/label/span[2]""","click",c,"xpath")
            with open('modules/craigslist.conf','r') as mod_:
                for param_ in mod_:
                    if param_.split(':')[0] == df.iat[x,7]:
                        sublocation = param_.split(':')[1]
                    elif param_.split(':')[0] == df.iat[x,1]:
                        category = param_.split(':')[1]
                    else: 
                        category = 1
            mod_.close()
            se.grab("""/html/body/article/section/form/ul/li["""+category+"""]/label/span[1]/input""","click",c,"xpath")
            try:
                se.grab("""/html/body/article/section/form/ul/li["""+sublocation+"""]/label/input""","click",c,"xpath")
            except:
                msg = " [!] No sublocation selected! This could mean there was none for your main city, or that something went wrong!"
                log_(msg)
            try:
                se.grab("""//*[@id="inputEmailHandle"]""","click",c,"xpath")
                se.keys(login[0],1,c)
                se.grab("""//*[@id="inputPassword"]""","click",c,"xpath")
                se.keys(login[1]+'\n',1,c)
            except:
                msg=" [!] Login didn't happen. Maybe logged-in already; don't worry about this error. Otherwise, double-check credentials.\n"
                log_(msg)
            
            try:
                se.grab("""/html/body/article/section/form/ul/li[1]/label/input""","click",c,"xpath")
            except:
                msg=" [!] No sublocation found, continuing without one for "+location+".\n"
                log_(msg)
                
            rand = random.randint(0,df.shape[0]-1)
            title_=df.iat[rand,4]
            se.grab("""//*[@id="PostingTitle"]""","click",c,"xpath")
            se.keys(title_,1,c)
            se.grab("""//*[@id="postal_code"]""","click",c,"xpath")
            se.keys(str(p_code),1,c)
            se.grab("""//*[@id="PostingBody"]""","click",c,"xpath")
            se.keys(body,1,c)
            if df.iat[x,6] != '':
                se.grab("""//*[@id="lic"]""","click",c,"xpath")
                se.grab("""//*[@id="license_info"]""","click",c,"xpath")
                se.keys(df.iat[x,6],1,c)
            se.grab("""//*[@id="wantamap"]""","click",c)
            se.grab("""/html/body/article/section/form/button""","click",c,"xpath")
            if df.iat[x,8] != '':
                images = []
                se.grab("""//*[@id="classic"]""","click",c)
                for each in str(os.listdir()+"/data/"+df.iat[x,8]+"/"):
                    images.append(each)
                for each in images:
                    selection = se.grab("""add""","select",c,"id")
                    selection.send_keys(str(os.listdir()+"/data/"+df.iat[x,8]+"/"+each))
                    time.sleep(2)
            se.grab("""/html/body/article/section/form/button""","click",c,"xpath")
            se.grab("""//*[@id="publish_bottom"]/button""","click",c,"xpath")
            x+=1
            time.sleep(3600)
