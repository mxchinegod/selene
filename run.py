import se
import sys
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def play(driver,instructions):
    print(driver)
    print(instructions)
    c = webdriver.Chrome(driver)
    c.implicitly_wait(10)
    se.browse("http://google.com",c)
    se.grab("""//*[@id="lst-ib"]""","click",c)
    se.keys("hello world",c,1)
    se.keys(Keys.ENTER,c,1)

#play(sys.argv[1],sys.argv[2])