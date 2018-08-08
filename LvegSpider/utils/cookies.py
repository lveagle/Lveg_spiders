#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-03 2:15
使用方法：
    获取cookie， get_cookie(site_key)
    存储cookie， save_cookie('cookies', site_key, get_cookie(site_key))
"""
import time
import json
import redis
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from LvegSpider.utils.yundama import identify

sites = {
    #'site_key': 'url'
    'survey_1dc': 'http://www.1diaocha.com/user/login.aspx',
}

def cookies_to_str(cookies):
    # 参数是cookie列表，即从Chrome driver.get_cookies返回的结果
    content = {}
    for cookie in cookies:
        content[cookie['name']] = cookie['value']
    return json.dumps(content)

def get_username_pasword_from_redis(site_key) ->tuple:
    r = redis.StrictRedis()
    username = r.hget('username-password', site_key).decode().split(':')[0]
    password = r.hget('username-password', site_key).decode().split(':')[1]
    return username,password


def get_cookie(site_key):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # driver = webdriver.Chrome()
    # 有界面浏览器，开发用

    # 通过selenium headless chrome 获取cookie，从这里开始------------------------------------------

    # ------------------------------ survey_1dc----------------------------------------
    if site_key == 'survey_1dc':
        driver.get(sites.get(site_key))
        username, password = get_username_pasword_from_redis(site_key)

        try:
            input_username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$inp_name")) )
            input_username.send_keys(username)
            # 一个等待就可以，因为是同一个页面上的元素
            input_password = driver.find_element_by_name('ctl00$ContentPlaceHolder1$inp_psd')
            input_password.send_keys(password)

            driver.find_element_by_id('ctl00_ContentPlaceHolder1_chkstate').click()
            driver.find_element_by_name('ctl00$ContentPlaceHolder1$login').click()
            time.sleep(2)

            # 处理弹窗，有点问题
            # TODO 想到的解决方法：登录两次，或者登录后刷新一次，待尝试
            try:
                driver.switch_to.alert().accept()
            except:
                pass
            return cookies_to_str(driver.get_cookies())

        except Exception as e:
            print(e)
        finally:
            driver.quit()

    # ------------------------------ survey_1dc----------------------------------------
    # 云打码测试
    if site_key =='survey_xxx':
        try:
            browser.save_screenshot("temp.png")
            code = browser.find_element_by_name("code")
            code.clear()
            from PIL import Image
            # 找到验证码
            img = browser.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
            # 获取验证码位置
            x = img.location["x"]
            y = img.location["y"]
            im = Image.open("temp.png")
            # 100, 40 为验证码图片大小，具体可F12查看
            im.crop((x, y, 100 + x, y + 40)).save("captcha.png")  # 剪切出验证码
            code_txt = identify()  # 验证码打码平台识别
            code.send_keys(code_txt)

        except:
            pass

def save_cookie(key, field, value):
    r = redis.StrictRedis()
    r.hset(key, field, value)

"""
if __name__ == '__main__':
    site_key = 'survey_1dc'
    # get_cookie(site_key)
    save_cookie('cookies', site_key, get_cookie(site_key))
"""
