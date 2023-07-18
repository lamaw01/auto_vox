from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

address = 'http://admin:paras4T@UC-1,Corp.@172.21.3.18/cgi-bin/php/system-status.php'
resetter_address = 'http://172.21.3.25/ovssh/index.php'
username = 'admin'
password = 'paras4T@UC-1,Corp.'
close_button = '//*[@id="modal-51"]/div/div/div[3]/button[1]'
table_element = '/html/body/div/div[5]/table[1]'
# port0 = '/html/body/div/div[5]/table[1]/tbody/tr[1]'
# port1 = '/html/body/div/div[5]/table[1]/tbody/tr[2]'
# port2 = '/html/body/div/div[5]/table[1]/tbody/tr[3]'
port_status_element = '/html/body/div/div[5]/table[1]/tbody/tr[2]/td[11]'

# x = 0
# y = 390

timeout = 10


#open vox
def open_vox():
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("detach", True)
        global driver_vox
        driver_vox = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        #set position and size
        # driver_vox.set_window_size(1152, 648)
        # driver_vox.set_window_position(x, y)
        driver_vox.get(address)
        wait_for_element_load(close_button,driver_vox)
        driver_vox.find_element(By.XPATH,close_button).click()
        time.sleep(10)
        # time.sleep(60)
        while True:
            scan()
            #wait 5:00 mins before refresh page
            time.sleep(300)
            #refresh page
            driver_vox.refresh()
            time.sleep(30)

    except Exception as e:
        print('open_vox',e)
        driver_vox.quit()

#function to ensure web element loaded
def wait_for_element_load(element, driver):
   element_wait_load = EC.presence_of_element_located((By.XPATH, element))
   WebDriverWait(driver, 10).until(element_wait_load)
   time.sleep(timeout)

def scan():
    print('scanning...')
    port_count = 1
    is_tail = False
    while is_tail is False:
        try:
            port_count = port_count + 1
            driver_vox.find_element(By.XPATH,table_element + '/tbody/tr' +  str([port_count])).click()
            port_name = driver_vox.find_element(By.XPATH,table_element + '/tbody/tr' + str([port_count]) + '/td[11]').text
            print(port_name)
            if port_name == 'INIT':
                open_resetter()
        except Exception as e:
            is_tail = True
            print('scan',e)
            
def open_resetter():
    print('open_resetter')
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("detach", True)
        # global driver_vox
        driver_resetter = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        #set position and size
        # driver_vox.set_window_size(1152, 648)
        # driver_vox.set_window_position(x, y)
        driver_resetter.get(resetter_address)
        time.sleep(60)

    except Exception as e:
        print('open_resetter',e)
        driver_resetter.quit()

open_vox()