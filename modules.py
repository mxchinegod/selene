import se, random, time
import pandas as pd
from selenium import webdriver
    
def craigslist(driver,instructions):
    
    c = webdriver.Chrome(driver)
    c.implicitly_wait(10)
    df = pd.read_csv(instructions)
    x=0
    login=[]
    for each in str(df.iat[0,5]).split(';'):
        login.append(each)
    for _ in range(df.shape[0]):
        location = df.iat[x,0]
        for _ in range(df.shape[1]):
            category = df.iat[x,1]
            p_code = df.iat[x,3]
            body = df.iat[x,2]
            se.browse("https://"+str(location)+".craigslist.org/search/"+str(category),c)
            se.grab("""//*[@id="page-top"]/header/div/ul[1]/li[1]/a""","click",c)
            se.grab("""/html/body/article/section/form/ul/li[10]/label/span[2]""","click",c)
            se.grab("""/html/body/article/section/form/ul/li[10]/label/span[2]""","click",c)
            
            try:
                se.grab("""//*[@id="inputEmailHandle"]""","click",c)
                se.keys(login[0],1,c)
                se.grab("""//*[@id="inputPassword"]""","click",c)
                se.keys(login[1]+'\n',1,c)
            except:
                with open("error.log", 'w') as error_log:
                    error_log.write(" [!] Login didn't happen. This could mean you're already logged in."+ 
                    " If so, don't worry about this error. Otherwise, double-check credentials.\n")
                error_log.close()
            
            try:
                se.grab("""/html/body/article/section/form/ul/li[1]/label/input""","click",c)
            except:
                with open("error.log", 'w') as error_log:
                    error_log.write(" [!] No sublocation found, continuing without one for "+location+".\n")
                error_log.close()
                
            rand = random.randint(0,df.shape[0]-1)
            title_=df.iat[rand,4]
            se.grab("""//*[@id="PostingTitle"]""","click",c)
            se.keys(title_,1,c)
            se.grab("""//*[@id="postal_code"]""","click",c)
            se.keys(str(p_code),1,c)
            se.grab("""//*[@id="PostingBody"]""","click",c)
            se.keys(body,1,c)
            se.grab("""//*[@id="wantamap"]""","click",c)
            se.grab("""/html/body/article/section/form/button""","click",c)
            se.grab("""/html/body/article/section/form/button""","click",c)
            se.grab("""//*[@id="publish_bottom"]/button""","click",c)
            x+=1
            time.sleep(3600)
