

import unittest, time, os
from appium import webdriver
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains

class Android_ATP_WTA(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['chromeOptions'] = {'androidPackage': 'com.android.chrome'}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = '$ Your device name'
        desired_caps['appPackage'] = 'com.google.android.gm'
        desired_caps['appActivity'] = "com.google.android.gm.ui.MailActivityGmail"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        "Tear down the test"
        self.driver.quit()

    def getUserPass(self):
        a = open("login.txt", "r")
        l = [line for line in a]
        return l

    def logout(self, user):
        sleep(15)
        self.driver.find_element_by_id("com.google.android.gm:id/action_done").click()
        sleep(5)
        self.driver.find_element_by_accessibility_id("Open navigation drawer").click()
        sleep(1)
        self.driver.find_element_by_id("com.google.android.gm:id/account_list_button").click()
        sleep(1)
        self.driver.find_element_by_id("com.google.android.gm:id/manage_accounts_text").click()
        sleep(2)
        self.driver.find_element_by_id("android:id/title").click()
        sleep(10)
        
        #self.driver.find_element_by_class_name("android.widget.LinearLayout[@index=6]").click()
        #self.driver.find_element_by_id("android:id/icon_frame").click()
        #print(self.driver.find_element_by_id("android:id/icon_frame"))
        #accounts = self.driver.find_element_by_class_name("android.widget.TextView")
        #a = [x for x in accounts if user == x.text()][0]
        #a.click()
        TouchAction(self.driver).tap(None, 600, 1650, 1).perform()
        sleep(5)
        def getMore():
             try:
                 sleep(1)
                 self.driver.find_element_by_accessibility_id("More options").click()
             except Exception:
                 TouchAction(self.driver).tap(None, 600, 1650, 1).perform()
                 getMore()
        getMore()       
        #sleep(1)
        #self.driver.find_element_by_accessibility_id("More options").click()
        sleep(10)
        #option = self.driver.find_element_by_class_name("android.widget.TextView")
        #o = [x for x in option if x.text() == "Remove account"][0]
        #o.click()
        TouchAction(self.driver).tap(None, 1100, 380, 1).perform()
        sleep(1)
        self.driver.find_element_by_id("android:id/button1").click()
        sleep(5)
        print("finished")
        
        
        
        
    def browser(self):
        sleep(5)
        self.driver.implicitly_wait(60)
        u = self.getUserPass()
        self.driver.find_element_by_id("identifierId").send_keys(u[0])
        sleep(2)
        self.driver.find_element_by_class_name("android.widget.EditText").send_keys(u[1])
        self.driver.find_element_by_id("passwordNext").click()
        sleep(2)

        try:
            self.driver.find_element_by_id("signinconsentNext").click()
        except Exception:
            pass
        self.logout(u[0])
        
    def getpin(self):
        a = open("pin.txt", "r")
        p = [line for line in a]
        return p[0]
    
    def typePin(self):
        pin = self.getpin()
        sleep(4)
        self.driver.find_element_by_id("com.android.settings:id/password_entry").send_keys(pin)
        self.driver.find_element_by_id("com.android.settings:id/next_button").click()
        
    def test(self):
        time.sleep(1)
        self.driver.find_element_by_id("com.google.android.gm:id/welcome_tour_got_it").click()
        time.sleep(1)
        self.driver.find_element_by_id("com.google.android.gm:id/setup_addresses_add_another").click()
        time.sleep(1)
        self.driver.find_element_by_id("com.google.android.gm:id/account_setup_item").click()
        self.typePin()
        self.browser()
               
#---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Android_ATP_WTA)
    unittest.TextTestRunner(verbosity=2).run(suite)
