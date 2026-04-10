import json
import pytest
from pageObjects.LoginPage import Loginpage
from pageObjects.ShoppingItems import Shopping

file_path = "C:\\Users\\grees\\PycharmProjects\\PythonTesting\\Python Selenium E-commerce application\\data\\E2E_datasets.json"
with open(file_path) as f:
    test_data = json.load(f)
    testlist= test_data["data"]          

@pytest.mark.smoke
@pytest.mark.parametrize("testlist_item", testlist)  
def test_EndtoEnd(browserInstance, env, testlist_item):     
    driver = browserInstance 

    lnd = Loginpage(driver)
    url = testlist_item["URLS"][env]
    lnd.landingPage(url)
    print(lnd.getTitle())       #parent inheritence
    shop = lnd.login(testlist_item["username"], testlist_item["email"], testlist_item["password"], testlist_item["DOB"],testlist_item["gender"]) 
    shop.ShoppingItems(testlist_item["gadget_name"])
    print(lnd.getTitle())
    check = shop.goToCart() 
    check.checkoutSummary()
    check.countryselection(testlist_item["country"])
    check.validate_order()
