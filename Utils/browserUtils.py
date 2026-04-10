

class BrowserUtils:

    def __init__(self, driver): #the moment u create a class initilize it from init method
        self.driver = driver

    def getTitle(self):
        return self.driver.title