#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-08 4:42
自动抓取文章，并且定时发布的程序
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
from selenium.webdriver.remote.webelement import WebElement

class Auto_article(object):

    sites = {
        'login': 'http://qqwz.site/wp/wp-login.php?redirect_to=http%3A%2F%2Fqqwz.site%2Fwp%2Fwp-admin%2F&reauth=1',
        'post': 'http://qqwz.site/wp/wp-admin/post-new.php',
    }

    def __init__(self, content, title, description, keywords):
        self.content = content
        self.title = title
        self.description = description
        self.keywords = keywords
        self.username, self.password = self.get_username_pasword_from_redis('qqwz.site')

    @staticmethod
    def get_username_pasword_from_redis(site_key) ->tuple:
        r = redis.StrictRedis()
        username = r.hget('username-password', site_key).decode().split(':')[0]
        password = r.hget('username-password', site_key).decode().split(':')[1]
        return username,password

    def publish(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(self.sites['login'])

        """
        input_username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$inp_name")) )
        input_username.send_keys(username)
        设置等待时间，可能要比较长
        """
        time.sleep(5)
        input_username = driver.find_element_by_id('user_login')
        input_username.clear()
        input_username.send_keys(self.username)

        input_password = driver.find_element_by_id('user_pass')
        input_password.clear()
        input_password.send_keys(self.password)

        driver.find_element_by_name('rememberme').click()
        driver.find_element_by_name('wp-submit').click()

        driver.get(self.sites['post'])
        time.sleep(2)

        # 输入标题
        input_title = driver.find_element_by_name('post_title')
        input_title.clear()
        input_title.send_keys(self.title)

        # 输入正文，需要进框架，然后返回，提示旧方法，但是新方法不管用，没办法
        # driver.switch_to_frame('content_ifr')
        # input_content = driver.find_element_by_id('tinymce')
        # input_content.send_keys(self.content)
        # driver.switch_to_default_content()
        input_content = driver.find_element_by_css_selector('.wp-editor-area')
        input_content.send_keys(self.content)
        time.sleep(2)

        # 输入SEO标题
        input_seo_title = driver.find_element_by_name('aiosp_title')
        input_seo_title.clear()
        input_seo_title.send_keys(self.title)

        # 输入描述
        input_description = driver.find_element_by_name('aiosp_description')
        input_description.clear()
        input_description.send_keys(self.description)

        # 输入keywords
        input_keywords = driver.find_element_by_name('aiosp_keywords')
        input_keywords.clear()
        input_keywords.send_keys(self.keywords)

        # 输入标签,同keywords
        input_tag = driver.find_element_by_name('newtag[post_tag]')
        input_tag.clear()
        input_tag.send_keys(self.keywords)
        driver.find_element_by_css_selector('.tagadd').click()
        time.sleep(2)

        # 选择日志模式
        driver.execute_script('$("#post-format-aside").click()')

        # 发布，被隐藏了，需要用JS发布
        # driver.execute_script("$document.getElementsByName('publish')[0].click()")
        driver.execute_script('$("#publish").click()')

        #退出
        time.sleep(2)
        driver.quit()


# 测试用
"""
# A = Auto_article('正文', '标题', '描述', '关键字')
A = Auto_article('我的正文', '我的标题', '我的描述', '我的关键字')
A.publish()
"""
