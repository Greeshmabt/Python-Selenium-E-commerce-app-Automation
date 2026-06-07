


import logging


class BrowserUtils:

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def getTitle(self):
        return self.driver.title