from selenium.webdriver.common.by import By

from Utils.browserUtils import BrowserUtils
from .CheckoutPage import CheckoutPage


class Shopping(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)    #it just setups parents driver, does not call any fn
        self.driver= driver
        self.shop_link= (By.LINK_TEXT, "Shop")
        self.allproducts= (By.XPATH, "//div[@class='card h-100']")
        self.checkout_button= (By.XPATH, "//a[@class='nav-link btn btn-primary']")

    def ShoppingItems(self, gadget_name):
        self.driver.find_element(*self.shop_link).click()
        self.driver.implicitly_wait(10)
        totalgadgets= self.driver.find_elements(*self.allproducts)

        for gadget in totalgadgets:
            gadgetName = gadget.find_element(By.XPATH,"div/h4/a").text
            if gadgetName == gadget_name:
                gadget.find_element(By.XPATH, "div/button").click()
                break
    def goToCart(self):
        self.driver.find_element(*self.checkout_button).click()
        #i know after goTocart() method ill landup in checksummary page so im creating its
        # object for class here itself n ill return it so that u can use in E2E
        check = CheckoutPage(self.driver)
        return check  #im returing this for E2E to use it directly





