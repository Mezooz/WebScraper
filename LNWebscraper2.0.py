#add firefox in firewall rules!
import os
from selenium import webdriver
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import webbrowser
#get user input for email and passwrd
userName = input('Please enter your OSU email: ')
userPasswrd = input('Please enter your OSU password: ')
search_list = []
#add searches to search list
while True:
    search = input("Enter a group to search for: ")
    search_list.append(search)
    cont = input("Do you want to search for another group as well? [y/n]: ")
    if cont == "y":
        continue
    elif cont == "n":
        break
    else:
        print("Please enter 'y' or 'n' next time...")
        continue
#iterate through search list and email results to specified email
for search in search_list:
    path_to_log = '/Users/mezooz/Desktop/'
    log_errors = open(path_to_log + 'log_errors.txt', mode = 'w')
    #this is for firefox TODO: make it for all browsers
    browser = webdriver.Firefox(executable_path="/Users/mezooz/Desktop/Python/WebScrapingTools/geckodriver")
    browser.implicitly_wait(10)
    url = 'https://login.argo.library.okstate.edu/login?qurl=http://www.lexisnexis.com%2fhottopics%2flnacademic%2f'
    browser.get(url)

    browser.find_element_by_id('txtInp_user_id0')
    browser.find_element_by_id('txtInp_user_id0').clear()
    browser.find_element_by_id('txtInp_user_id0').send_keys(userName)
    browser.find_element_by_id('pwdinp_pass_id0')
    browser.find_element_by_id('pwdinp_pass_id0').clear()
    browser.find_element_by_id('pwdinp_pass_id0').send_keys(userPasswrd)
    browser.find_element_by_css_selector('.btn.btn-primary.btn-lg').click()

    browser.switch_to_frame('mainFrame')
    browser.find_element_by_id('terms')
    browser.find_element_by_id('terms').clear()
    browser.find_element_by_id("terms").send_keys(search)
    browser.find_element_by_id('srchButt').click()
    #sometimes a warning comes up
    try:
        browser.find_element_by_xpath("//img[@title='Warning']")
        print(search + " isn't turning up...")
        browser.quit()
        continue
    except:
        browser.switch_to_default_content()
        browser.switch_to_frame('mainFrame')
        dyn_frame = browser.find_elements_by_xpath('//frame[contains(@name, "fr_resultsNav")]')
        framename = dyn_frame[0].get_attribute('name') 
        browser.switch_to_frame(framename)
        docs = int(browser.find_element_by_name('totalDocsInResult').get_attribute('value'))
    #LN doesnt let you email more than 500 docs at a time, so split it up
        if docs <= 500:
            browser.find_element_by_css_selector('img[alt=\"Email Documents\"]').click()
            browser.switch_to_default_content()
            browser.switch_to_window(browser.window_handles[1])
            browser.find_element_by_xpath('//select[@id="sendAs"]/option[text()="Attachment"]').click()
            browser.find_element_by_xpath('//select[@id="delFmt"]/option[text()="Text"]').click()
            browser.find_element_by_name('emailTo').clear()
            browser.find_element_by_name('emailTo').send_keys(userName)                     
            browser.find_element_by_id('emailNote').clear()
            browser.find_element_by_id('emailNote').send_keys(search)
            browser.find_element_by_id('all').click()
            browser.find_element_by_css_selector('img[alt=\"Send\"]').click()
            print("Finishing up...")
            browser.quit()
        elif docs > 500:
            initial = 1
            final = 500
            count = 0
            while final <= docs and final >= initial:
                count += 1
                browser.find_element_by_css_selector('img[alt=\"Email Documents\"]').click()
                browser.switch_to_default_content()
                browser.switch_to_window(browser.window_handles[1])
                browser.find_element_by_xpath('//select[@id="sendAs"]/option[text()="Attachment"]').click()
                browser.find_element_by_xpath('//select[@id="delFmt"]/option[text()="Text"]').click()
                browser.find_element_by_name('emailTo').clear()
                browser.find_element_by_name('emailTo').send_keys(userName)						
                browser.find_element_by_id('emailNote').clear()
                browser.find_element_by_id('emailNote').send_keys(search)
                browser.find_element_by_id('sel').click()
                browser.find_element_by_id('rangetextbox').clear()
                browser.find_element_by_id('rangetextbox').send_keys('{}-{}'.format(initial, final))
                browser.find_element_by_css_selector('img[alt=\"Send\"]').click()
                try:
                    element = WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt=\"Close Window\"]')))
                except TimeoutException:
                    log_errors.write('oops, TimeoutException when searching for your search' + '\n')
                    seconds = 5 + (random.random() * 5)
                    time.sleep(seconds)
                initial += 500
                if final + 500 > docs:
                    final = docs
                else:
                    final += 500
                backwindow = browser.window_handles[0]
                browser.switch_to_window(backwindow)
                browser.switch_to_default_content()
                browser.switch_to_frame('mainFrame')
                framelist = browser.find_elements_by_xpath('//frame[contains(@name, "fr_resultsNav")]')
                framename = framelist[0].get_attribute('name')
                browser.switch_to_frame(framename)
                print("Finishing up....")
browser.quit()
print("All done! Check your email!")






