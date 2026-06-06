import json
import pytest
from pageObjects.LoginPage import Loginpage
from pageObjects.ShoppingItems import Shopping
from Utils.logging_utils import LoggingUtils

# This is just for logs
logger = LoggingUtils.setup_logger("test.log")

# Taking data from json file
file_path = "C:\\Users\\grees\\PycharmProjects\\PythonTesting\\Python Selenium E-commerce application\\data\\E2E_datasets.json"
with open(file_path) as f:
    test_data = json.load(f)
    testlist= test_data["data"]          #u need to pass ur key here and store as list

@pytest.mark.smoke
@pytest.mark.parametrize("testlist_item", testlist)   #im storing test list into a variable testlist_item
def test_EndtoEnd(browserInstance, env, testlist_item):     #here u need to pass testlist_item because ur parameterizing it so use variables
    driver = browserInstance  # browserInstance IS the driver
    logger.info("Starting end-to-end test")
    lnd = Loginpage(driver)
    url = testlist_item["URLS"][env]   #i passed the key here n the env i pass from cmd QA or UAT
    lnd.landingPage(url) #passing QA or UAT url into landing page
    print(lnd.getTitle())       #got this method from parent inheritence of Loginpage
    shop = lnd.login(testlist_item["username"], testlist_item["email"], testlist_item["password"], testlist_item["DOB"],testlist_item["gender"])  #i have chained login and shopping
    shop.ShoppingItems(testlist_item["gadget_name"])
    print(lnd.getTitle())
    check = shop.goToCart()  #i have chained gotocart and checkout
    check.checkoutSummary()
    check.countryselection(testlist_item["country"])
    check.validate_order()
    logger.info("Test completed successfully")

#config file fixtures are used in E2E pytest file only,
# all page objects inherit only utils parent class which has driver