from Utils.browserUtils import BrowserUtils
from .ShoppingItems import Shopping
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class Loginpage(BrowserUtils):     #nheritance from parent class

    def __init__(self, driver):    #initializing current class
        super().__init__(driver)   #initializing parent class as well
        self.driver = driver
        self.username_input= (By.NAME, "name")
        self.email_input= (By.NAME, "email")
        self.password_input= (By.ID, "exampleInputPassword1")
        self.checkbox_input= (By.ID, "exampleCheck1")
        self.radio_input= (By.ID, "inlineRadio2")
        self.bday_input= (By.NAME, "bday")
        self.gender_input= (By.ID, "exampleFormControlSelect1")
        self.submit_btn= (By.CSS_SELECTOR, "input[value='Submit']")
        self.alertsuccess= (By.CLASS_NAME, "alert.alert-success") #packing locators into tuple
        self.base_url= "base_url"

    def landingPage(self, base_url):
        self.driver.get(base_url)

    def login(self, username, email, password, DOB, gender):
        self.driver.find_element(*self.username_input).send_keys(username) # *is used to unpack the tuple into 2 arguments
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.checkbox_input).click()
        self.driver.find_element(*self.radio_input).click()
        self.driver.find_element(*self.bday_input).send_keys(DOB)
        Select(self.driver.find_element(*self.gender_input)).select_by_visible_text(gender)
        self.driver.find_element(*self.submit_btn).click()
        msg = self.driver.find_element(*self.alertsuccess).text
        print(msg)
        assert "Success" in msg
        #after login() method i know ill landup in shopping page so im calling that object here itself and itll return it
        shop = Shopping(self.driver)
        return shop  #returing shop so that u can use it in E2E without calling its class there
