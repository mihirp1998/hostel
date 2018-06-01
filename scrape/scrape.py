from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys
#import org.openqa.selenium.chrome.ChromeDriver;
import unittest, time, re

class Sel(unittest.TestCase):
    def setUp(self):
	#System.setProperty("webdriver.chrome.driver", "~/chromedriver");
        self.driver = webdriver.Chrome("../chromedriver")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.scribd.com/doc/144272571/Options-as-a-Strategic-Investment"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        driver = self.driver
        delay = 3
	print("no")
        driver.get(self.base_url + "/search?q=stckoverflow&src=typd")
        # driver.find_element_by_link_text("All").click()
        print("hello")
	for i in range(1,2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
	print data

if __name__ == "__main__":
    unittest.main()
