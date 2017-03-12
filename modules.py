import se, random, time, os
import pandas as pd
from selenium import webdriver

def log(msg):

    with open("error.log", 'a') as error_log:
        error_log.write(msg+'\n')
        error_log.close()

def craigslist(driver,instructions,timer):

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
            phone = df.iat[x,9]
            contact = df.iat[x,10]
            se.browse("https://"+str(location)+".craigslist.org/",c)
            se.grab("""//*[@id="post"]""","click",c,"xpath")
            se.grab("""/html/body/article/section/form/ul/li[10]/label/span[2]""","click",c,"xpath")

            with open('modules/craigslist.conf','r') as mod_:
                for param_ in mod_:
                    print(param_)
                    if param_.split(':')[0] == df.iat[x,7]:
                        sublocation = param_.split(':')[1]
                        print(sublocation)
                    elif param_.split(':')[0] == df.iat[x,1]:
                        category = param_.split(':')[1]
                        print(category)
                    else:
                        pass
            mod_.close()

            try:
                se.grab("""/html/body/article/section/form/ul/li["""+str(category)+"""]/label/span[1]/input""","click",c,"xpath")
            except:
                msg = " [!] No category selected! This could mean there was none for your main city, or that something went wrong!"
                log(msg)
                category = 1
                se.grab("""/html/body/article/section/form/ul/li["""+str(sublocation)+"""]/label/input""","click",c,"xpath")

            try:
                se.grab("""//*[@id="inputEmailHandle"]""","click",c,"xpath")
                se.keys(login[0],1,c)
                se.grab("""//*[@id="inputPassword"]""","click",c,"xpath")
                se.keys(login[1]+'\n',1,c)
            except:
                msg=" [!] Login didn't happen. Maybe logged-in already; don't worry about this error. Otherwise, double-check credentials.\n"
                log(msg)

            try:
                se.grab("""/html/body/article/section/form/ul/li["""+str(sublocation)+"""]/label/input""","click",c,"xpath")
            except:
                msg = " [!] No sublocation selected! This could mean there was none for your main city, or that something went wrong!"
                log(msg)
                sublocation = 1
                se.grab("""/html/body/article/section/form/ul/li["""+str(sublocation)+"""]/label/input""","click",c,"xpath")

            rand = random.randint(0,df.shape[0]-1)
            title_=df.iat[rand,4]
            se.grab("""//*[@id="PostingTitle"]""","click",c,"xpath")
            se.keys(title_,1,c)
            se.grab("""//*[@id="postal_code"]""","click",c,"xpath")
            se.keys(str(p_code),1,c)
            se.grab("""//*[@id="PostingBody"]""","click",c,"xpath")
            se.keys(body,1,c)
            if df.iat[x,9] != '':
                se.grab("""//*[@id="contact_phone"]""","click",c,"xpath")
                se.keys(df.iat[x,9].split(";")[0],1,c)
                if df.iat[x,9].split(';')[1] == "call":
                    se.grab("""//*[@id="contact_phone_ok"]""","click",c,"xpath")
                elif df.iat[x,9].split(";")[1] == "text":
                    se.grab("""//*[@id="contact_text_ok"]""","click",c,"xpath")
                elif df.iat[x,9].split(";")[1] == "both":
                    se.grab("""//*[@id="contact_text_ok"]""","click",c,"xpath")
                    se.grab("""//*[@id="contact_phone_ok"]""","click",c,"xpath")
            if df.iat[x,10] != '':
                if df.iat[x,10] == "none":
                    se.grab("""//*[@id="A"]""","click",c,"xpath")
                elif df.iat[x,10] == "real":
                    se.grab("""//*[@id="P"]""","click",c,"xpath")
                elif df.iat[x,10] == "relay":
                    se.grab("""//*[@id="oiab"]/label[1]/input""","click",c,"xpath")
            if df.iat[x,6] != '':
                se.grab("""//*[@id="lic"]""","click",c,"xpath")
                se.grab("""//*[@id="license_info"]""","click",c,"xpath")
                se.keys(df.iat[x,6],1,c)
            else:
                msg = " [!] No license info found in the instructions! Continuing, hopefully this isn't a mistake."
                log(msg)
            se.grab("""//*[@id="mapinfo"]/fieldset/legend/label""","click",c,"xpath")
            se.grab("""//*[@id="postingForm"]/div/button""","click",c,"xpath")
            try:
                if df.iat[x,8] != '':
                    images = []
                    se.grab("""//*[@id="classic"]""","click",c,"xpath")
                    for each in os.listdir(os.getcwd()+"\\\\data\\\\"+str(df.iat[x,8])):
                        images.append(each)
                        for image in images:
                            print(image)
                            selection = se.grab("""input[type="file" i]""","select",c,"css")
                            selection.send_keys(str(os.getcwd()+"\\\\data\\\\"+df.iat[x,8]+"\\\\"+image))
                            time.sleep(1)
            except:
                log(" [!] Image upload didn't happen. Check your path and that you have images in that path.")
            se.grab("""/html/body/article/section/form/button""","click",c,"xpath")
            se.grab("""//*[@id="publish_bottom"]/button""","click",c,"xpath")
            x+=1
            time.sleep(timer)
