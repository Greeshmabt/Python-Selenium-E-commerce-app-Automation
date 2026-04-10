from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from Utils.browserUtils import BrowserUtils


class CheckoutPage (BrowserUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.checkout_summary= (By.XPATH,"//button[@class='btn btn-success']")
        self.country= (By.ID, "country")
        self.checkbox= (By.XPATH, "//div[@class='checkbox checkbox-primary']")
        self.purchase_btn= (By.XPATH, "//input[@type='submit']")
        self.successbooking= (By.CLASS_NAME, "alert-success")
        self.mobile_incart= (By.CSS_SELECTOR, "h4.media-heading")

    def checkoutSummary(self):

        m= self.driver.find_element(*self.mobile_incart).text
        print(m)    # i wanted to print which mobile was there in cart
        self.driver.find_element(*self.checkout_summary).click()  # this is checkout button in checkout summary of items page.

    def countryselection(self,country_name):
        self.driver.find_element(*self.country).send_keys(country_name)
        wait = WebDriverWait(self.driver, 10)
        # Create dynamic locator based on country_name parameter
        countyName = (By.LINK_TEXT, country_name)
        wait.until(expected_conditions.element_to_be_clickable(countyName))
        self.driver.find_element(*countyName).click()
        self.driver.find_element(*self.checkbox).click()
        self.driver.find_element(*self.purchase_btn).click()

    def validate_order(self):
        wait = WebDriverWait(self.driver, 15)
        wait.until(expected_conditions.visibility_of_element_located(self.successbooking))
        smsg= self.driver.find_element(*self.successbooking).text
        assert "Success!" in smsg
