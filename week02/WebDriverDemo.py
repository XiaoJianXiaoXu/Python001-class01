from selenium import webdriver
import time

browser = webdriver.Chrome()

# 登录
def weibo_login(username, password):
    browser.get('https://shimo.im/login?from=home')
    browser.implicitly_wait(5)
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys(username)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys(password)
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()
    time.sleep(1)

username = 'xxxxx@163.com'
password = "xxxxs"
weibo_login(username, password)
