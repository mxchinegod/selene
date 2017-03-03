from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from modules import log_

def grab(send,act,c,element):
    

    if element == "xpath":
        
        if act == "select":
            try:
                selection = c.find_element_by_xpath(send)
                return selection
            except:
                error = "There was an error selecting an object by xpath!"
                log_(error)
                
        if act == "click":
            try:
                c.find_element_by_xpath(send).click()
            except:
                error = "There was an error clicking an object!"
                log_(error)
            
        elif act == "href":
            try:
                href = c.find_element_by_xpath(send).get_attribute("href")
                return href
            except:
                error = "There was an error retrieving the <a> tag of an object!"
                log_(error)
            
        elif act == "text":
            try:
                text = c.find_element_by_xpath(send).text
                return text
            except:
                error = "There was an error getting the text value of an object!"
                log_(error)
                
    if element == "class":
        
        if act == "select":
            try:
                selection = c.find_element_by_class(send)
                return selection
            except:
                error = "There was an error selecting an object by class!"
                log_(error)
                
        if act == "click":
            try:
                c.find_element_by_class(send).click()
            except:
                error = "There was an error clicking an object!"
                log_(error)
            
        elif act == "href":
            try:
                href = c.find_element_by_class(send).get_attribute("href")
                return href
            except:
                error = "There was an error retrieving the <a> tag of an object!"
                log_(error)
            
        elif act == "text":
            try:
                text = c.find_element_by_class(send).text
                return text
            except:
                error = "There was an error getting the text value of an object!"
                log_(error)
    
    if element == "id":
        
        if act == "select":
            try:
                selection = c.find_element_by_id(send)
                return selection
            except:
                error = "There was an error selecting an object by id!"
                log_(error) 
                
        if act == "click":
            try:
                c.find_element_by_id(send).click()
            except:
                error = "There was an error clicking an object!"
                log_(error)
            
        elif act == "href":
            try:
                href = c.find_element_by_id(send).get_attribute("href")
                return href
            except:
                error = "There was an error retrieving the <a> tag of an object!"
                log_(error)
            
        elif act == "text":
            try:
                text = c.find_element_by_id(send).text
                return text
            except:
                error = "There was an error getting the text value of an object!"
                log_(error)        
        
def browse(url,c):
    
    c.get(url)
    
    
def keys(keys,x,c):
    
    actions = ActionChains(c)
    
    if keys=="ENTER":
        for _ in range(x):
            actions = actions.send_keys(Keys.ENTER)
            
    elif keys=="TAB":
        for _ in range(x):
            actions = actions.send_keys(Keys.TAB)

    elif keys=="DOWN":
        for _ in range(x):
            actions = actions.send_keys(Keys.DOWN)            
    else:
        for _ in range(x):
            actions = actions.send_keys(keys)
            
    actions.perform()
