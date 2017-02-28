from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def grab(xpath,act,c):
    
    if act == "click":
        
        try:
            
            c.find_element_by_xpath(xpath).click()
            
        except:
            
            error = "There was an error clicking an object!"
            return error
        
    elif act == "href":
        
        try:
            
            href = c.find_element_by_xpath(xpath).get_attribute("href")
            return href
        
        except:
            
            error = "There was an error retrieving the <a> tag of an object!"
            return error
        
    elif act == "text":
        
        try:
            
            text = c.find_element_by_xpath(xpath).text
            return text
        
        except:
            
            error = "There was an error getting the text value of an object!"
            return error
        
        
def browse(url,c):
    
    c.get(url)
    
    
def keys(keys,c,x):
    
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
